"""
Slack MCP Tool for SmolAgent integration
"""

from typing import Any
from smolagents import Tool
from mcp.connector import MCPConnector


class SlackMCPTool(Tool):
    """Slack MCP tool that provides Slack operations via MCP protocol"""
    
    name = "slack_mcp"
    description = """A Slack integration tool that can read messages, send messages, send images, and interact with Slack channels.
    Requires proper Slack bot token configuration."""
    
    inputs = {
        "operation": {
            "type": "string",
            "description": "The Slack operation to perform. Available operations: list_channels, send_message, send_image, get_messages"
        },
        "channel": {
            "type": "string", 
            "description": "Slack channel ID (starts with C). Required for most operations.",
            "nullable": True
        },
        "message": {
            "type": "string",
            "description": "Message text to send. Required for send_message operation, optional for send_image.",
            "nullable": True
        },
        "image_path": {
            "type": "string",
            "description": "Local file path to image to upload. Required for send_image operation.",
            "nullable": True
        },
        "limit": {
            "type": "integer",
            "description": "Number of messages to retrieve. Optional for get_messages.",
            "nullable": True
        }
    }
    output_type = "object"
    
    def __init__(self):
        super().__init__()
        self.mcp_connector = None
        self._server_started = False
        
    def _ensure_server_started(self):
        """Ensure the Slack MCP server is running"""
        if not self._server_started:
            try:
                self.mcp_connector = MCPConnector()
                success = self.mcp_connector.start_server("slack")
                if success:
                    self._server_started = True
                    # Give server time to initialize
                    import time
                    time.sleep(2)
                    return True
                else:
                    return False
            except Exception as e:
                print(f"❌ Failed to start Slack MCP server: {e}")
                return False
        return True
    
    def _send_mcp_request(self, method: str, params: dict) -> dict:
        """Send an MCP request to the Slack server"""
        if not self._ensure_server_started():
            return {"error": "Failed to start Slack MCP server"}
            
        try:
            # Get the process for the Slack server
            if "slack" not in self.mcp_connector.active_processes:
                return {"error": "Slack server not running"}
                
            process = self.mcp_connector.active_processes["slack"]
            
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
    
    def forward(self, operation: str, channel: str = None, message: str = None, image_path: str = None, limit: int = None) -> dict:
        """Execute Slack operations via MCP protocol"""
        
        try:
            if operation == "list_channels":
                return self._list_channels()
            elif operation == "send_message":
                return self._send_message(channel, message)
            elif operation == "send_image":
                return self._send_image(channel, image_path, message)
            elif operation == "get_messages":
                return self._get_messages(channel, limit)
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}",
                    "available_operations": ["list_channels", "send_message", "send_image", "get_messages"]
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Slack operation failed: {str(e)}"
            }
    
    def _list_channels(self) -> dict:
        """List Slack channels"""
        response = self._send_mcp_request("tools/call", {
            "name": "slack_list_channels",
            "arguments": {}
        })
        
        if "error" not in response and response.get("result"):
            try:
                import json
                result_content = response["result"]
                if isinstance(result_content, dict) and "content" in result_content:
                    # Extract JSON string from content
                    json_text = result_content["content"][0]["text"]
                    slack_data = json.loads(json_text)
                    
                    if slack_data.get("ok"):
                        return {
                            "success": True,
                            "channels": slack_data.get("channels", [])
                        }
                    else:
                        return {
                            "success": False,
                            "error": slack_data.get("error", "Slack API error")
                        }
                else:
                    return {
                        "success": True,
                        "channels": result_content
                    }
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                return {
                    "success": False,
                    "error": f"Failed to parse Slack response: {str(e)}",
                    "raw_response": response.get("result")
                }
        else:
            return {
                "success": False,
                "error": response.get("error", "Failed to list channels"),
                "details": response
            }
    
    def _send_message(self, channel: str, message: str) -> dict:
        """Send a message to a Slack channel"""
        if not channel or not message:
            return {
                "success": False,
                "error": "Both channel and message parameters are required for send_message operation"
            }
            
        params = {
            "channel_id": channel,
            "text": message
        }
        response = self._send_mcp_request("tools/call", {
            "name": "slack_post_message",
            "arguments": params
        })
        
        if "error" not in response and response.get("result"):
            try:
                import json
                result_content = response["result"]
                if isinstance(result_content, dict) and "content" in result_content:
                    # Extract JSON string from content
                    json_text = result_content["content"][0]["text"]
                    slack_data = json.loads(json_text)
                    
                    if slack_data.get("ok"):
                        return {
                            "success": True,
                            "message_sent": slack_data,
                            "channel": channel
                        }
                    else:
                        return {
                            "success": False,
                            "error": slack_data.get("error", "Slack API error"),
                            "channel": channel
                        }
                else:
                    return {
                        "success": True,
                        "message_sent": result_content,
                        "channel": channel
                    }
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                return {
                    "success": False,
                    "error": f"Failed to parse Slack response: {str(e)}",
                    "raw_response": response.get("result")
                }
        else:
            return {
                "success": False,
                "error": response.get("error", "Failed to send message"),
                "details": response
            }
    
    def _get_messages(self, channel: str, limit: int = None) -> dict:
        """Get messages from a Slack channel"""
        if not channel:
            return {
                "success": False,
                "error": "Channel parameter is required for get_messages operation"
            }
            
        params = {"channel_id": channel}
        if limit:
            params["limit"] = limit
            
        response = self._send_mcp_request("tools/call", {
            "name": "slack_get_channel_history",
            "arguments": params
        })
        
        if "error" not in response and response.get("result"):
            # Parse the JSON response from the MCP server
            try:
                import json
                result_content = response["result"]
                if isinstance(result_content, dict) and "content" in result_content:
                    # Extract JSON string from content
                    json_text = result_content["content"][0]["text"]
                    slack_data = json.loads(json_text)
                    
                    if slack_data.get("ok"):
                        return {
                            "success": True,
                            "messages": slack_data.get("messages", []),
                            "channel": channel,
                            "has_more": slack_data.get("has_more", False)
                        }
                    else:
                        return {
                            "success": False,
                            "error": slack_data.get("error", "Slack API error"),
                            "channel": channel
                        }
                else:
                    return {
                        "success": True,
                        "messages": result_content,
                        "channel": channel
                    }
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                return {
                    "success": False,
                    "error": f"Failed to parse Slack response: {str(e)}",
                    "raw_response": response.get("result")
                }
        else:
            return {
                "success": False,
                "error": response.get("error", "Failed to get messages"),
                "details": response
            }
    
    def _send_image(self, channel: str, image_path: str, message: str = None) -> dict:
        """Send an image to a Slack channel using file upload"""
        if not channel:
            return {
                "success": False,
                "error": "Channel parameter is required for send_image operation"
            }
            
        if not image_path:
            return {
                "success": False,
                "error": "image_path parameter is required for send_image operation"
            }
        
        # Check if file exists
        import os
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"Image file not found: {image_path}"
            }
        
        try:
            # Since the Slack MCP server doesn't have file upload, 
            # we'll implement a direct Slack API call using the new upload method
            import json
            import urllib.request
            import urllib.parse
            
            # Get bot token from environment or MCP connector
            bot_token = None
            
            # First try to get from MCP connector if available
            if self.mcp_connector and hasattr(self.mcp_connector, 'servers') and "slack" in self.mcp_connector.servers:
                bot_token = self.mcp_connector.servers["slack"].env.get("SLACK_BOT_TOKEN")
            
            # Fallback to environment variable
            if not bot_token:
                import os
                bot_token = os.environ.get("SLACK_BOT_TOKEN")
            
            # Last resort: try loading from .env file directly
            if not bot_token:
                try:
                    with open('.env', 'r') as f:
                        for line in f:
                            if line.startswith('SLACK_BOT_TOKEN='):
                                bot_token = line.split('=', 1)[1].strip()
                                break
                except FileNotFoundError:
                    pass
            
            if not bot_token:
                return {
                    "success": False,
                    "error": "SLACK_BOT_TOKEN not found in environment or .env file"
                }
            
            # Read and encode the image
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Get file info
            filename = os.path.basename(image_path)
            file_size = len(image_data)
            
            # Step 1: Get upload URL using the new Slack API
            upload_url_response = urllib.request.Request(
                'https://slack.com/api/files.getUploadURLExternal',
                data=urllib.parse.urlencode({
                    'filename': filename,
                    'length': file_size
                }).encode('utf-8'),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': f'Bearer {bot_token}'
                }
            )
            
            with urllib.request.urlopen(upload_url_response) as response:
                upload_data = json.loads(response.read().decode('utf-8'))
            
            if not upload_data.get('ok'):
                return {
                    "success": False,
                    "error": f"Failed to get upload URL: {upload_data.get('error', 'Unknown error')}",
                    "details": upload_data
                }
            
            # Step 2: Upload file to the external URL
            upload_url = upload_data['upload_url']
            file_id = upload_data['file_id']
            
            upload_request = urllib.request.Request(
                upload_url,
                data=image_data,
                headers={
                    'Content-Type': 'application/octet-stream'
                }
            )
            
            with urllib.request.urlopen(upload_request) as response:
                if response.status != 200:
                    return {
                        "success": False,
                        "error": f"Failed to upload file. Status: {response.status}"
                    }
            
            # Step 3: Complete the upload and share to channel
            complete_request = urllib.request.Request(
                'https://slack.com/api/files.completeUploadExternal',
                data=urllib.parse.urlencode({
                    'files': json.dumps([{
                        'id': file_id,
                        'title': filename
                    }]),
                    'channel_id': channel,
                    'initial_comment': message or ''
                }).encode('utf-8'),
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': f'Bearer {bot_token}'
                }
            )
            
            with urllib.request.urlopen(complete_request) as response:
                response_data = json.loads(response.read().decode('utf-8'))
            
            if response_data.get('ok'):
                return {
                    "success": True,
                    "file_uploaded": response_data,
                    "channel": channel,
                    "filename": filename
                }
            else:
                return {
                    "success": False,
                    "error": response_data.get('error', 'File upload failed'),
                    "details": response_data
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to upload image: {str(e)}"
            }

    def __del__(self):
        """Cleanup: stop MCP server when tool is destroyed"""
        if self.mcp_connector and self._server_started:
            try:
                self.mcp_connector.stop_server("slack")
            except Exception:
                pass  # Ignore cleanup errors
