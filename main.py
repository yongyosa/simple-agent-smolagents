#!/usr/bin/env python3

"""
Main entry point for the Simple Agent with Calculator and Excel Tools.
"""

from agent import SimpleAgent
import os


def main():
    """Main function to demonstrate the agent's capabilities."""
    print("🤖 Enhanced SmolAgent with Calculator & Excel Tools")
    print("=" * 60)
    
    # Create temp directory for Excel files
    temp_dir = "./temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Initialize agent
    agent = SimpleAgent()
    
    print("🔧 Available Tools:")
    print("1. 🔢 Calculator Tool - Mathematical operations")
    print("2. 📊 Excel Tool - Create, read, and modify Excel files")
    print("3. ⏰ Time Tool - Date/time operations and timezone conversions")
    print("4. 💬 Slack Tool - Read and send messages in Slack channels")
    print()
    
    # Test questions demonstrating all tools
    # test_questions = [
    #     # Excel examples
    #     f"Create an Excel file at '{temp_dir}/budget.xlsx' with my expenses: Rent 1200, Food 400, Transport 150",
    #     f"""Read the data from '{temp_dir}/budget.xlsx', then do the following tasks: 
    #         1. Double the food amount and calculate the total expenses. 
    #         2. Add date time now (CET) to all entries. 
    #         3. Then, write the result back to the file with name budget_modify.xlsx""",
    # ]

    # Slack example with image upload
    test_questions = [
        "Please send the file 'temp_files/sample_calendar.png' to Slack channel 'C09H5KW3475' with the message 'Here is our sample calendar!'"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n🧪 Test {i}: {question}")
        print("🤖 Processing...")
        
        try:
            response = agent.run(question)
            print(f"✅ Answer: {response}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 60)
    
    print("\n🎉 Demo completed! Check the temp_files directory for created Excel files.")


if __name__ == "__main__":
    main()
