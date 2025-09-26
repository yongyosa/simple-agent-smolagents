#!/usr/bin/env python3

"""
MCP Connector Demonstration with Excel MCP Server
"""

import sys
import os
# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from mcp.connector import MCPConnector, create_sample_excel_config


def main():
    """Demonstrate MCP connector functionality with Excel server"""
    print("🔌 MCP Connector Demonstration")
    print("=" * 50)
    
    # Create sample config if it doesn't exist
    try:
        connector = MCPConnector()
    except FileNotFoundError:
        print("📝 Creating sample MCP configuration...")
        create_sample_excel_config()
        connector = MCPConnector()
    
    # Display available servers
    print(f"📋 Available MCP servers: {connector.list_servers()}")
    
    # Get Excel server info
    excel_server = connector.get_server_info("excel")
    if excel_server:
        print("📊 Excel server config:")
        print(f"   Command: {excel_server.command}")
        print(f"   Args: {excel_server.args}")
        print(f"   Environment: {excel_server.env}")
    
    # Check initial status
    print(f"📊 Excel server status: {connector.get_server_status('excel')}")
    
    # Start Excel server
    print("\n🚀 Starting Excel MCP server...")
    success = connector.start_server("excel")
    
    if success:
        print("✅ Server started successfully!")
        
        # Wait a moment for initialization
        print("⏳ Waiting for server initialization...")
        time.sleep(3)
        
        # Check status again
        status = connector.get_server_status("excel")
        print(f"📊 Current status: {status}")
        
        # List active servers
        active_servers = connector.list_active_servers()
        print(f"🟢 Active servers: {active_servers}")
        
        # Test the server
        print("\n🧪 Testing Excel server...")
        test_result = connector.test_excel_server()
        
        if test_result:
            print("\n✅ Excel MCP server is ready for use!")
            print("🔗 Next steps:")
            print("   1. The server is now running and ready to accept connections")
            print("   2. You can integrate this with your SmolAgent")
            print("   3. Available Excel operations include:")
            print("      - create_workbook: Create new Excel files")
            print("      - read_cells: Read cell values from Excel files") 
            print("      - write_cells: Write data to Excel cells")
            print("      - And more Excel operations...")
        
        # Keep server running for a bit to show it's working
        print("\n⏰ Keeping server running for 10 seconds...")
        time.sleep(10)
        
        # Clean shutdown
        print("\n🛑 Stopping Excel server...")
        connector.stop_server("excel")
        
    else:
        print("❌ Failed to start Excel server")
        print("💡 Troubleshooting tips:")
        print("   1. Make sure Node.js and npm are installed")
        print("   2. Check your internet connection (npx needs to download packages)")
        print("   3. Verify the Excel MCP server package is available")
    
    print("\n🏁 Demo completed!")


def interactive_demo():
    """Interactive demonstration mode"""
    print("🎮 Interactive MCP Demo Mode")
    print("=" * 30)
    
    connector = MCPConnector()
    
    while True:
        print("\nAvailable commands:")
        print("1. List servers")
        print("2. Start Excel server")
        print("3. Stop Excel server") 
        print("4. Check server status")
        print("5. Test Excel server")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            print(f"📋 Available servers: {connector.list_servers()}")
            print(f"🟢 Active servers: {connector.list_active_servers()}")
            
        elif choice == "2":
            print("🚀 Starting Excel server...")
            success = connector.start_server("excel")
            if success:
                print("✅ Server started!")
            else:
                print("❌ Failed to start server")
                
        elif choice == "3":
            print("🛑 Stopping Excel server...")
            success = connector.stop_server("excel")
            if success:
                print("✅ Server stopped!")
            else:
                print("❌ Failed to stop server")
                
        elif choice == "4":
            status = connector.get_server_status("excel")
            print(f"📊 Excel server status: {status}")
            
        elif choice == "5":
            print("🧪 Testing Excel server...")
            result = connector.test_excel_server()
            if result:
                print("✅ Test passed!")
            else:
                print("❌ Test failed!")
                
        elif choice == "6":
            print("👋 Cleaning up and exiting...")
            connector.stop_all_servers()
            break
            
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_demo()
    else:
        main()
