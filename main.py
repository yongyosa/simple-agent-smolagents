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
    print()
    
    # Test questions demonstrating both tools
    test_questions = [
        # Calculator examples
        "What is 15 + 25?",
        "Can you multiply 7 by 8?", 
        "Calculate 100 divided by 4 and then add 10",
        
        # Excel examples
        f"Create an Excel file at '{temp_dir}/budget.xlsx' with my expenses: Rent 1200, Food 400, Transport 150",
        f"Read the data from '{temp_dir}/budget.xlsx' and calculate the total expenses",
        
        # Combined example
        "Calculate 25% of 2000 and create an Excel file with the result"
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
