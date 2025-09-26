#!/usr/bin/env python3

"""
Main entry point for the Simple Agent with Calculator Tool.
"""

from agent import SimpleAgent


def main():
    """Main function to test the simple agent."""
    print("🤖 Simple Agent with Calculator Tool")
    print("=" * 50)
    
    # Initialize agent
    agent = SimpleAgent()
    
    # Test questions
    test_questions = [
        "What is 15 + 25?",
        "Can you multiply 7 by 8?", 
        "What's 100 divided by 4?",
        "Calculate 50 minus 17",
        "Hello! Can you help me with some math?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print(f"🤖 Answer: {agent.run(question)}")
        print("-" * 40)


if __name__ == "__main__":
    main()
