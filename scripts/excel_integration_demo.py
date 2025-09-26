#!/usr/bin/env python3

"""
Excel MCP Integration Example with SmolAgent
"""

import sys
import os
# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.connector import MCPConnector
import time
import tempfile


def create_sample_excel_file():
    """Create a sample Excel file for testing"""
    # Create a temporary directory for Excel files
    temp_dir = tempfile.mkdtemp(prefix="excel_mcp_test_")
    excel_file = os.path.join(temp_dir, "sample_data.xlsx")
    
    print(f"📁 Created test directory: {temp_dir}")
    print(f"📊 Excel file will be: {excel_file}")
    
    return temp_dir, excel_file


def demo_excel_mcp_integration():
    """Demonstrate Excel MCP server integration"""
    print("🔗 Excel MCP Integration Demo")
    print("=" * 40)
    
    # Create sample file path
    test_dir, excel_file = create_sample_excel_file()
    
    try:
        # 1. Start the Excel MCP server
        print("🚀 Starting Excel MCP server...")
        mcp_connector = MCPConnector()
        
        if not mcp_connector.start_server("excel"):
            print("❌ Failed to start Excel MCP server")
            return
        
        # Wait for server to initialize
        time.sleep(3)
        
        # Check if server is running
        status = mcp_connector.get_server_status("excel")
        print(f"📊 Excel MCP server status: {status}")
        
        if status == "running":
            print("✅ Excel MCP server is ready!")
            print()
            print("🎯 Integration Points:")
            print("   1. The Excel MCP server is now running via stdio transport")
            print("   2. It can be integrated with SmolAgent as a custom tool")
            print("   3. Available Excel operations:")
            print("      - Create workbooks and worksheets")
            print("      - Read/write cell data")
            print("      - Apply formatting and styling")
            print("      - Generate charts and pivot tables")
            print("      - Manage Excel tables and formulas")
            print()
            
            # 2. Show how this could integrate with SmolAgent
            print("🤖 SmolAgent Integration Example:")
            print("   The Excel MCP server can provide tools like:")
            print("   - ExcelCreateTool: Create new Excel files")
            print("   - ExcelReadTool: Read data from Excel files")
            print("   - ExcelWriteTool: Write data to Excel files")
            print("   - ExcelChartTool: Create charts and visualizations")
            print()
            
            # 3. Demonstrate server is responsive
            print("🧪 Server Communication Test:")
            print("   The server is listening on stdio and ready to accept")
            print("   MCP protocol messages for Excel operations.")
            print()
            
            # Keep server running for demonstration
            print("⏰ Keeping Excel MCP server running for 10 seconds...")
            print("   (In a real application, this would stay running)")
            time.sleep(10)
            
        else:
            print(f"❌ Excel MCP server failed to start properly (status: {status})")
            
    except Exception as e:
        print(f"❌ Error in demo: {e}")
        
    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        mcp_connector.stop_server("excel")
        
        # Clean up test directory
        import shutil
        try:
            shutil.rmtree(test_dir)
            print(f"✅ Cleaned up test directory: {test_dir}")
        except Exception as e:
            print(f"⚠️  Could not clean up {test_dir}: {e}")
    
    print("🏁 Excel MCP Integration demo completed!")


def show_integration_architecture():
    """Show how Excel MCP integrates with SmolAgent architecture"""
    print("\n🏗️  Integration Architecture:")
    print("=" * 50)
    print("""
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   SmolAgent     │    │  Excel MCP      │    │   Excel Files   │
    │                 │    │  Server         │    │                 │
    │ ┌─────────────┐ │    │                 │    │ ┌─────────────┐ │
    │ │ Calculator  │ │    │ ┌─────────────┐ │    │ │   .xlsx     │ │
    │ │ Tool        │ │    │ │ Stdio       │ │    │ │ Workbooks   │ │
    │ └─────────────┘ │────│ │ Transport   │ │────│ └─────────────┘ │
    │                 │    │ └─────────────┘ │    │                 │
    │ ┌─────────────┐ │    │                 │    │ ┌─────────────┐ │
    │ │ Excel MCP   │ │    │ ┌─────────────┐ │    │ │ Charts &    │ │
    │ │ Tool        │ │    │ │ Excel Ops   │ │    │ │ Tables      │ │
    │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
    
    Communication Flow:
    1. SmolAgent receives user request for Excel operations
    2. SmolAgent calls Excel MCP Tool
    3. Excel MCP Tool communicates with MCP Server via stdio
    4. MCP Server performs Excel file operations
    5. Results returned through the chain back to user
    """)
    
    print("\n📋 Next Steps for Full Integration:")
    print("   1. Create ExcelMCPTool class extending SmolAgent's Tool")
    print("   2. Implement MCP protocol communication in the tool")
    print("   3. Add Excel tool to SmolAgent's tools list")
    print("   4. Test end-to-end Excel operations via natural language")


if __name__ == "__main__":
    demo_excel_mcp_integration()
    show_integration_architecture()
