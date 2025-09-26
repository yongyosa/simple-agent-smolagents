# Simple Agent with Calculator Tool

A minimal implementation of an AI agent using SmolAgent with LiteLLM via AWS Bed## Project Structure

```
simple-agent-smolagents/
├── main.py                    # Entry point and test examples
├── agent.py                   # SimpleAgent and LiteLLMModel classes
├── agent_tools/
│   ├── __init__.py
│   └── calculator.py          # Calculator tool implementation
├── mcp/
│   ├── __init__.py
│   ├── connector.py           # MCP connector for Excel server
│   └── mcp_servers.json       # MCP server configurations
├── prompts/
│   ├── __init__.py
│   └── templates.py           # Professional prompt templates
├── scripts/
│   ├── mcp_demo.py           # MCP connector demonstration
│   └── excel_integration_demo.py  # Excel MCP integration example
├── requirements.txt           # Dependencies
├── setup.sh                   # Environment setup script
└── README.md                  # This file
```

## Usage

### Basic Agent Usagecalculator tool.

## Features

- 🤖 **SmolAgent**: Uses the SmolAgent framework for agent functionality
- 🔢 **Calculator Tool**: Simple arithmetic operations (add, subtract, multiply, divide)  
- ☁️ **AWS Bedrock**: LiteLLM integration with AWS Bedrock Claude model
- 🎯 **Custom Prompts**: Professional prompt templates similar to enterprise systems
- 📝 **Template System**: Jinja2-based template rendering for dynamic prompts
- 🚀 **Simple Setup**: Minimal configuration required

## Demo

The agent successfully handles natural language math questions:

```
❓ Question: What is 15 + 25?
🤖 Answer: 40

❓ Question: Can you multiply 7 by 8?
🤖 Answer: 56

❓ Question: What's 100 divided by 4?
🤖 Answer: 25.0
```

## Prerequisites

- Python 3.8+
- AWS credentials configured (for Bedrock access)
- AWS region with Bedrock Claude access

## Quick Start

### 1. Setup Environment

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### 2. Configure AWS Credentials

Make sure your AWS credentials are configured. You can use:

```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### 3. Run the Agent

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the simple agent
python main.py
```

## Usage

### Basic Usage

The agent can handle natural language math questions:

- "What is 15 + 25?"
- "Can you multiply 7 by 8?"
- "What's 100 divided by 4?"
- "Calculate 50 minus 17"

### Programmatic Usage

You can also import and use the agent in your own code:

```python
from agent import SimpleAgent

# Initialize agent
agent = SimpleAgent()

# Ask a question
response = agent.run("What is 20 + 15?")
print(response)  # Output: 35
```

## Architecture

The agent follows a modular architecture:

- **main.py**: Entry point with test examples and main function
- **agent.py**: Core agent implementation with `SimpleAgent` and `LiteLLMModel` classes
- **agent_tools/calculator.py**: Modular calculator tool implementation
- **prompts/templates.py**: Professional prompt template system

## Configuration

You can customize the agent by modifying the `SimpleAgent` class initialization:

```python
# Use different model or region
agent = SimpleAgent(
    model_id="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
    aws_region_name="us-west-2"
)
```

## Project Structure

```
simple-agent-smolagents/
├── main.py                    # Entry point and test examples
├── agent.py                   # SimpleAgent and LiteLLMModel classes
├── agent_tools/
│   ├── __init__.py
│   └── calculator.py          # Calculator tool implementation
├── prompts/
│   ├── __init__.py
│   └── templates.py           # Professional prompt templates
├── requirements.txt           # Dependencies
├── setup.sh                   # Environment setup script
└── README.md                  # This file
```

### Prompt Template System
- **Action Planning Template**: Guides the agent's reasoning and code generation
- **Tool Description Template**: Dynamic rendering of available tools
- **SmolAgent Templates**: Planning, managed agents, and final answer formatting
- **Jinja2 Integration**: Professional template rendering with variable substitution

### Agent Components
- **LiteLLMModel**: Custom model adapter for AWS Bedrock integration
- **CalculatorTool**: Example tool following SmolAgent patterns
- **Template Rendering**: Dynamic prompt generation based on available tools

## Dependencies

- `litellm`: LLM gateway for AWS Bedrock integration
- `smolagents`: Agent framework (v1.17.0 - matches enterprise template)
- `boto3`: AWS SDK for Python
- `jinja2`: Template engine for dynamic prompt generation

## Advanced Usage

### Customizing Prompts

You can modify the prompt templates in `prompts/templates.py` to customize agent behavior:

```python
# Example: Adding domain-specific examples to the action planning template
action_planning_template = """
    You are an expert mathematical assistant...
    
    Here are examples for your domain:
    - Financial calculations
    - Scientific computations
    - Statistical analysis
"""
```

### Adding New Tools

Follow the SmolAgent pattern to add new tools:

```python
class NewTool(Tool):
    name = "new_tool"
    description = "Description of what this tool does"
    inputs = {
        "param1": {
            "type": "string",
            "description": "Parameter description"
        }
    }
    output_type = "string"

    def forward(self, param1: str) -> str:
        # Tool implementation
        return f"Result: {param1}"
```

## Troubleshooting

### AWS Bedrock Access
- Ensure you have access to Claude models in your AWS region
- Check that your IAM user/role has Bedrock permissions
- Verify the model ID is correct for your region

### Environment Issues
- Make sure virtual environment is activated
- Check Python version (3.8+ required)
- Reinstall dependencies if needed: `pip install -r requirements.txt`

### MCP (Model Context Protocol) Integration

The project includes a simple MCP connector for Excel operations:

```bash
# Run MCP demonstration
python scripts/mcp_demo.py

# Run Excel integration demo  
python scripts/excel_integration_demo.py

# Interactive MCP demo
python scripts/mcp_demo.py --interactive
```

The MCP connector supports:
- Excel file operations (create, read, write)
- Chart and pivot table generation
- Cell formatting and styling
- Integration with SmolAgent framework
