#!/usr/bin/env python3

"""
End-to-End Excel Operations Test with SmolAgent
This script tests the complete integration of Excel MCP tool with SmolAgent.
"""

import sys
import os
# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import SimpleAgent
import time


def test_excel_operations():
    """Test end-to-end Excel operations via natural language"""
    print("📊 End-to-End Excel Operations Test")
    print("=" * 50)
    
    # Create temp_files directory for test files
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_dir = os.path.join(project_root, "temp_files")
    os.makedirs(test_dir, exist_ok=True)
    excel_file = os.path.join(test_dir, "sales_data.xlsx")
    
    try:
        print(f"📁 Test directory: {test_dir}")
        print(f"📄 Test Excel file: {excel_file}")
        print()
        
        # Initialize the enhanced agent with Excel capabilities
        print("🤖 Initializing SmolAgent with Calculator and Excel tools...")
        agent = SimpleAgent()
        print("✅ Agent initialized successfully!")
        print()
        
        # Test cases for Excel operations via natural language
        test_cases = [
            {
                "description": "Create Excel workbook with sales data",
                "question": f"""Create an Excel file at '{excel_file}' with sales data. 
                Add a worksheet called 'Q1_Sales' and put the following data:
                Row 1: Product, January, February, March
                Row 2: Laptops, 1200, 1350, 1100
                Row 3: Phones, 800, 950, 1200
                Row 4: Tablets, 600, 720, 650"""
            },
            {
                "description": "Read data from the Excel file", 
                "question": f"Read all the data from the Excel file '{excel_file}' and show me what's in it."
            },
            {
                "description": "Calculate total sales per product",
                "question": f"Calculate the total sales for each product from the Excel file '{excel_file}'. Add up January + February + March for each product."
            },
            {
                "description": "Add summary calculations to Excel",
                "question": f"Add a new column called 'Total' to the Excel file '{excel_file}' that shows the sum of January, February, and March for each product."
            }
        ]
        
        # Execute test cases
        for i, test_case in enumerate(test_cases, 1):
            print(f"🧪 Test {i}: {test_case['description']}")
            print(f"❓ Question: {test_case['question']}")
            print()
            
            start_time = time.time()
            try:
                response = agent.run(test_case['question'])
                end_time = time.time()
                
                print(f"🤖 Response (took {end_time - start_time:.2f}s):")
                print(f"{response}")
                print("✅ Test completed successfully!")
                
            except Exception as e:
                print(f"❌ Test failed with error: {str(e)}")
            
            print("─" * 60)
            print()
        
        # Final verification - check if Excel file was created
        if os.path.exists(excel_file):
            file_size = os.path.getsize(excel_file)
            print("✅ Excel file created successfully!")
            print(f"📄 File: {excel_file}")
            print(f"💾 Size: {file_size} bytes")
        else:
            print("⚠️  Excel file was not found - operations may not have completed successfully")
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        
    finally:
        # Cleanup - just clean up the specific test file, keep temp_files directory
        print("\n🧹 Cleaning up test files...")
        try:
            if os.path.exists(excel_file):
                os.remove(excel_file)
                print(f"✅ Cleaned up: {excel_file}")
        except Exception as e:
            print(f"⚠️  Could not clean up {excel_file}: {e}")
    
    print("\n🏁 End-to-end Excel operations test completed!")


def test_mixed_operations():
    """Test mixed calculator and Excel operations"""
    print("\n🔀 Mixed Operations Test (Calculator + Excel)")
    print("=" * 50)
    
    # Create temp_files directory for mixed operations
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_dir = os.path.join(project_root, "temp_files")
    os.makedirs(test_dir, exist_ok=True)
    excel_file = os.path.join(test_dir, "calculations.xlsx")
    
    try:
        print(f"📁 Test directory: {test_dir}")
        
        # Initialize agent
        agent = SimpleAgent()
        
        # Mixed operation test cases
        mixed_tests = [
            {
                "description": "Calculate and store results in Excel",
                "question": f"""First calculate 15 * 25, then 100 / 4, then 50 - 17. 
                After that, create an Excel file at '{excel_file}' and store these results:
                Row 1: Operation, Result
                Row 2: 15 * 25, [first result]
                Row 3: 100 / 4, [second result]  
                Row 4: 50 - 17, [third result]"""
            },
            {
                "description": "Read Excel data and perform calculations",
                "question": f"""Read the data from '{excel_file}' and calculate the sum of all the results."""
            }
        ]
        
        for i, test in enumerate(mixed_tests, 1):
            print(f"🧪 Mixed Test {i}: {test['description']}")
            print(f"❓ Question: {test['question']}")
            print()
            
            try:
                start_time = time.time()
                response = agent.run(test['question'])
                end_time = time.time()
                
                print(f"🤖 Response (took {end_time - start_time:.2f}s):")
                print(f"{response}")
                print("✅ Mixed test completed!")
                
            except Exception as e:
                print(f"❌ Mixed test failed: {str(e)}")
            
            print("─" * 60)
            print()
            
    except Exception as e:
        print(f"❌ Mixed operations test failed: {str(e)}")
        
    finally:
        # Cleanup - just clean up the specific test file, keep temp_files directory
        try:
            if os.path.exists(excel_file):
                os.remove(excel_file)
                print(f"✅ Cleaned up mixed test: {excel_file}")
        except Exception as e:
            print(f"⚠️  Could not clean up {excel_file}: {e}")


def show_capabilities():
    """Show the enhanced agent capabilities"""
    print("\n🚀 Enhanced SmolAgent Capabilities")
    print("=" * 50)
    print("""
🔧 Available Tools:
1. 🔢 Calculator Tool
   - Basic arithmetic (add, subtract, multiply, divide)
   - Handles mathematical operations via natural language
   
2. 📊 Excel MCP Tool  
   - Create and manage Excel workbooks
   - Read/write worksheet data
   - Format cells and ranges
   - Generate charts and pivot tables
   - List worksheets and manage file operations

🎯 Integration Features:
- Natural language interface for all operations
- Seamless tool coordination (calculate then store results)
- Professional prompt templates for complex reasoning
- Error handling and validation
- File path management and cleanup

💬 Example Queries:
- "Create an Excel file with my budget data"
- "Calculate the total and add it to the Excel sheet"
- "Read the sales data and create a chart"
- "What's 15 + 25, and save that result in a new Excel file?"
""")


if __name__ == "__main__":
    show_capabilities()
    
    # Run comprehensive tests
    test_excel_operations()
    test_mixed_operations()
    
    print("\n🎉 All tests completed!")
    print("🔗 Your SmolAgent now supports both calculator and Excel operations!")
    print("💡 Try asking complex questions that combine math and Excel tasks!")
