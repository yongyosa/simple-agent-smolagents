"""
Calculator tool for basic arithmetic operations.
"""

from smolagents import Tool


class CalculatorTool(Tool):
    """Simple calculator tool that can perform basic arithmetic operations."""
    
    name = "calculator"
    description = "A calculator tool that can perform basic arithmetic operations like addition, subtraction, multiplication, and division."
    inputs = {
        "operation": {
            "type": "string",
            "description": "The arithmetic operation to perform. Can be 'add', 'subtract', 'multiply', or 'divide'."
        },
        "a": {
            "type": "number",
            "description": "The first number"
        },
        "b": {
            "type": "number", 
            "description": "The second number"
        }
    }
    output_type = "number"

    def forward(self, operation: str, a: float, b: float) -> float:
        """Execute the calculation based on the operation type."""
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operation: {operation}. Supported operations: add, subtract, multiply, divide")
