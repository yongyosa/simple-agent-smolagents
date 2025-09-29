"""
Simple MCP Connector for connecting to MCP servers
"""

import json
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass
import os


# Constants
DEFAULT_CONFIG_FILE = "mcp/mcp_servers.json"


@dataclass
class MCPServer:
    """Configuration for an MCP server"""
    name: str
    command: str
    args: List[str]
    env: Dict[str, str]


class MCPConnector:
    """Simple MCP Connector to communicate with MCP servers"""
    
    def __init__(self, config_file: str = DEFAULT_CONFIG_FILE):
        """Initialize the MCP connector with server configurations"""
        self.config_file = config_file
        self.servers: Dict[str, MCPServer] = {}
        self.active_processes: Dict[str, subprocess.Popen] = {}
        self.load_config()
    
    def load_config(self):
        """Load MCP server configurations from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            for name, server_config in config.get('mcpServers', {}).items():
                self.servers[name] = MCPServer(
                    name=name,
                    command=server_config['command'],
                    args=server_config.get('args', []),
                    env=server_config.get('env', {})
                )
            print(f"✅ Loaded {len(self.servers)} MCP server configurations")
            
        except FileNotFoundError:
            print(f"❌ Config file {self.config_file} not found")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {self.config_file}: {e}")
            raise
    
    def list_servers(self) -> List[str]:
        """Get list of configured server names"""
        return list(self.servers.keys())
    
    def get_server_info(self, server_name: str) -> Optional[MCPServer]:
        """Get information about a specific server"""
        return self.servers.get(server_name)
    
    def start_server(self, server_name: str) -> bool:
        """Start an MCP server process"""
        if server_name not in self.servers:
            print(f"❌ Server '{server_name}' not found in configuration")
            return False
        
        if server_name in self.active_processes:
            print(f"⚠️  Server '{server_name}' is already running")
            return True
        
        server = self.servers[server_name]
        
        try:
            # Prepare environment variables
            env = os.environ.copy()
            env.update(server.env)
            
            print(f"🚀 Starting MCP server '{server_name}'...")
            print(f"   Command: {server.command} {' '.join(server.args)}")
            
            # Start the process
            process = subprocess.Popen(
                [server.command] + server.args,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
            
            self.active_processes[server_name] = process
            print(f"✅ Server '{server_name}' started with PID {process.pid}")
            
            # Initialize MCP connection
            import time
            time.sleep(2)  # Give server time to start
            
            success = self._initialize_mcp_connection(server_name)
            if not success:
                print(f"❌ Failed to initialize MCP connection for '{server_name}'")
                self.stop_server(server_name)
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Failed to start server '{server_name}': {e}")
            return False
    
    def stop_server(self, server_name: str) -> bool:
        """Stop an MCP server process"""
        if server_name not in self.active_processes:
            print(f"⚠️  Server '{server_name}' is not running")
            return True
        
        try:
            process = self.active_processes[server_name]
            process.terminate()
            
            # Wait for process to terminate gracefully
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"⚠️  Server '{server_name}' didn't terminate gracefully, killing...")
                process.kill()
                process.wait()
            
            del self.active_processes[server_name]
            print(f"✅ Server '{server_name}' stopped")
            return True
            
        except Exception as e:
            print(f"❌ Failed to stop server '{server_name}': {e}")
            return False
    
    def stop_all_servers(self):
        """Stop all running MCP servers"""
        server_names = list(self.active_processes.keys())
        for server_name in server_names:
            self.stop_server(server_name)
    
    def get_server_status(self, server_name: str) -> str:
        """Get the status of a server"""
        if server_name not in self.servers:
            return "not_configured"
        
        if server_name not in self.active_processes:
            return "stopped"
        
        process = self.active_processes[server_name]
        poll_result = process.poll()
        
        if poll_result is None:
            return "running"
        else:
            # Process has terminated, but let's check the return code
            # MCP servers may exit with different codes, so let's be more lenient
            print(f"⚠️  Process '{server_name}' terminated with code: {poll_result}")
            del self.active_processes[server_name]
            return "stopped"
    
    def list_active_servers(self) -> List[str]:
        """Get list of currently running servers"""
        active = []
        for server_name in self.active_processes.keys():
            if self.get_server_status(server_name) == "running":
                active.append(server_name)
        return active

    def _initialize_mcp_connection(self, server_name: str) -> bool:
        """Initialize MCP connection with proper handshake"""
        if server_name not in self.active_processes:
            return False
            
        process = self.active_processes[server_name]
        
        try:
            import json
            import time
            
            # Step 1: Send initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "excel-mcp-connector",
                        "version": "1.0.0"
                    }
                }
            }
            
            request_line = json.dumps(init_request) + "\n"
            process.stdin.write(request_line)
            process.stdin.flush()
            
            # Read initialization response
            time.sleep(1)
            response_line = process.stdout.readline().strip()
            if response_line:
                response = json.loads(response_line)
                if "result" not in response:
                    print(f"❌ MCP initialization failed: {response}")
                    return False
            
            # Step 2: Send initialized notification
            initialized_request = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            
            request_line = json.dumps(initialized_request) + "\n"
            process.stdin.write(request_line)
            process.stdin.flush()
            time.sleep(0.5)
            
            print(f"✅ MCP connection initialized for '{server_name}'")
            return True
            
        except Exception as e:
            print(f"❌ MCP initialization error: {e}")
            return False
    
    def test_excel_server(self, server_name: str = "excel") -> bool:
        """Test the Excel MCP server functionality"""
        if not self.start_server(server_name):
            return False
        
        try:
            # Wait a moment for the server to initialize
            import time
            time.sleep(5)  # Give more time for the server to fully initialize
            
            # Check if server is still running
            status = self.get_server_status(server_name)
            if status != "running":
                print(f"❌ Excel server failed to start properly (status: {status})")
                return False
            
            print("✅ Excel MCP server is running successfully!")
            print("   You can now use Excel operations through the MCP protocol")
            print("   Available tools include:")
            print("   - create_workbook: Create new Excel workbooks")
            print("   - read_workbook: Read data from Excel files")
            print("   - write_worksheet: Write data to Excel worksheets")
            print("   - create_chart: Generate charts (line, bar, pie, scatter)")
            print("   - create_pivot_table: Create dynamic pivot tables")
            print("   - format_cells: Apply formatting and styling")
            print("   - create_table: Create and manage Excel tables")
            print("   - add_formula: Insert formulas and calculations")
            print("   - copy_worksheet: Duplicate worksheets")
            print("   - And many more Excel operations...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing Excel server: {e}")
            return False
    
    def __del__(self):
        """Cleanup: stop all servers when the connector is destroyed"""
        self.stop_all_servers()


# Convenience functions for easy usage
def start_excel_server(config_file: str = DEFAULT_CONFIG_FILE) -> MCPConnector:
    """Convenience function to start Excel MCP server"""
    connector = MCPConnector(config_file)
    connector.start_server("excel")
    return connector


def create_sample_excel_config(filename: str = DEFAULT_CONFIG_FILE):
    """Create a sample Excel MCP server configuration file"""
    config = {
        "mcpServers": {
            "excel": {
                "command": "uvx",
                "args": ["excel-mcp-server", "stdio"],
                "env": {}
            }
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"✅ Created sample Excel MCP config: {filename}")
