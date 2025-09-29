"""
Time MCP Tool for SmolAgent integration
"""

from typing import Any
from smolagents import Tool
from mcp.connector import MCPConnector


class TimeMCPTool(Tool):
    """Time MCP tool that provides date/time operations via MCP protocol"""
    
    name = "time_mcp"
    description = """A time and date tool that can get current time, format dates, and perform time zone operations.
    Supports getting current time, converting between time zones, and formatting dates."""
    
    inputs = {
        "operation": {
            "type": "string",
            "description": "The time operation to perform. Available operations: get_current_time, convert_time"
        },
        "timezone": {
            "type": "string",
            "description": "Timezone name (e.g., 'UTC', 'America/New_York', 'Europe/London'). Optional for some operations.",
            "nullable": True
        },
        "format": {
            "type": "string", 
            "description": "Date/time format string (e.g., '%Y-%m-%d %H:%M:%S'). Optional.",
            "nullable": True
        },
        "timestamp": {
            "type": "string",
            "description": "ISO timestamp string for operations that need input time. Optional.",
            "nullable": True
        },
        "time": {
            "type": "string",
            "description": "Time in 24-hour format (HH:MM) for convert_time operation. Optional.",
            "nullable": True
        },
        "source_timezone": {
            "type": "string",
            "description": "Source timezone for convert_time operation. Optional.",
            "nullable": True
        },
        "target_timezone": {
            "type": "string",
            "description": "Target timezone for convert_time operation. Optional.",
            "nullable": True
        }
    }
    output_type = "object"
    
    def __init__(self):
        super().__init__()
        self.mcp_connector = None
        self._server_started = False
        
    def _ensure_server_started(self):
        """Ensure the Time MCP server is running"""
        if not self._server_started:
            try:
                self.mcp_connector = MCPConnector()
                success = self.mcp_connector.start_server("time")
                if success:
                    self._server_started = True
                    # Give server time to initialize
                    import time
                    time.sleep(2)
                    return True
                else:
                    return False
            except Exception as e:
                print(f"❌ Failed to start Time MCP server: {e}")
                return False
        return True
    
    def _send_mcp_request(self, method: str, params: dict) -> dict:
        """Send an MCP request to the Time server"""
        if not self._ensure_server_started():
            return {"error": "Failed to start Time MCP server"}
            
        try:
            # Get the process for the Time server
            if "time" not in self.mcp_connector.active_processes:
                return {"error": "Time server not running"}
                
            process = self.mcp_connector.active_processes["time"]
            
            # Construct MCP request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params
            }
            
            # Send request via stdin
            import json
            request_line = json.dumps(request) + "\n"
            process.stdin.write(request_line)
            process.stdin.flush()
            
            # Read response from stdout
            import time
            time.sleep(1)
            
            response_line = process.stdout.readline().strip()
            if response_line:
                try:
                    response = json.loads(response_line)
                    return response
                except json.JSONDecodeError:
                    return {"error": f"Invalid JSON response: {response_line}"}
            else:
                return {"error": "No response from MCP server"}
            
        except Exception as e:
            return {"error": f"MCP communication error: {str(e)}"}
    
    def forward(self, operation: str, timezone: str = None, format: str = None, timestamp: str = None, 
               time: str = None, source_timezone: str = None, target_timezone: str = None) -> dict:
        """Execute time operations via MCP protocol"""
        
        try:
            if operation == "get_current_time":
                return self._get_current_time(timezone, format)
            elif operation == "convert_time":
                return self._convert_time(source_timezone, time, target_timezone)
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}",
                    "available_operations": ["get_current_time", "convert_time"]
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Time operation failed: {str(e)}"
            }
    
    def _get_current_time(self, timezone: str = None, format: str = None) -> dict:
        """Get current time"""
        # Default timezone if none provided (time server requires timezone)
        timezone = timezone or "UTC"
        
        params = {"timezone": timezone}
        if format:
            params["format"] = format
            
        response = self._send_mcp_request("tools/call", {
            "name": "get_current_time",
            "arguments": params
        })
        
        if "error" not in response and response.get("result"):
            return {
                "success": True,
                "current_time": response["result"],
                "timezone": timezone
            }
        else:
            return {
                "success": False,
                "error": response.get("error", "Failed to get current time"),
                "details": response
            }
    
    def _convert_time(self, source_timezone: str, time: str, target_timezone: str) -> dict:
        """Convert time between timezones"""
        if not all([source_timezone, time, target_timezone]):
            return {
                "success": False,
                "error": "source_timezone, time, and target_timezone parameters are required for convert_time operation"
            }
            
        params = {
            "source_timezone": source_timezone,
            "time": time,
            "target_timezone": target_timezone
        }
        response = self._send_mcp_request("tools/call", {
            "name": "convert_time",
            "arguments": params
        })
        
        if "error" not in response and response.get("result"):
            return {
                "success": True,
                "conversion_result": response["result"],
                "source_timezone": source_timezone,
                "target_timezone": target_timezone
            }
        else:
            return {
                "success": False,
                "error": response.get("error", "Failed to convert time"),
                "details": response
            }
    
    def __del__(self):
        """Cleanup: stop MCP server when tool is destroyed"""
        if self.mcp_connector and self._server_started:
            try:
                self.mcp_connector.stop_server("time")
            except Exception:
                pass  # Ignore cleanup errors
