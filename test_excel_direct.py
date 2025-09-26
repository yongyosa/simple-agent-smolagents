#!/usr/bin/env python3

"""
Test Excel MCP server directly to see what's happening
"""

import subprocess
import time
import json


def test_excel_mcp_direct():
    """Test the Excel MCP server directly to see output"""
    print("🧪 Testing Excel MCP Server Direct Connection")
    print("=" * 50)
    
    try:
        # Start the process and capture output
        print("🚀 Starting Excel MCP server...")
        process = subprocess.Popen(
            ["npx", "--yes", "@negokaz/excel-mcp-server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            env={
                **dict(os.environ),
                "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
            }
        )
        
        print(f"✅ Process started with PID: {process.pid}")
        
        # Wait a moment and check if it's still running
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Process is still running!")
            
            # Try to send an initialization message (MCP protocol)
            init_message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            print("📤 Sending initialization message...")
            process.stdin.write(json.dumps(init_message) + "\n")
            process.stdin.flush()
            
            # Try to read response
            time.sleep(1)
            
            # Read any available output
            import select
            import sys
            
            if hasattr(select, 'select'):
                ready, _, _ = select.select([process.stdout], [], [], 1)
                if ready:
                    output = process.stdout.readline()
                    print(f"📥 Response: {output.strip()}")
                else:
                    print("⏳ No immediate response received")
            
            # Terminate the process
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Process terminated gracefully")
            except subprocess.TimeoutExpired:
                process.kill()
                print("⚠️  Process killed after timeout")
                
        else:
            # Process has already terminated
            returncode = process.returncode
            stdout, stderr = process.communicate()
            
            print(f"❌ Process terminated with code: {returncode}")
            if stdout:
                print(f"📤 STDOUT:\n{stdout}")
            if stderr:
                print(f"📤 STDERR:\n{stderr}")
                
    except Exception as e:
        print(f"❌ Error testing Excel MCP server: {e}")


if __name__ == "__main__":
    import os
    test_excel_mcp_direct()
