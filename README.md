# Enhanced SmolAgent with Calculator, Excel, and Time Tools

A comprehensive implementation of an AI agent using SmolAgent with LiteLLM via AWS Bedrock, featuring calculator, Excel, and time operations through MCP (Model Context Protocol).

## Features

- 🤖 **SmolAgent**: Uses the SmolAgent framework for intelligent agent functionality
- 🔢 **Calculator Tool**: Arithmetic operations (add, subtract, multiply, divide)  
- 📊 **Excel MCP Tool**: Complete Excel operations via Model Context Protocol
  - Create and manage workbooks
  - Read/write worksheet data  
  - Format cells and ranges
  - Generate charts and pivot tables
- ⏰ **Time MCP Tool**: Date and time operations via Model Context Protocol
  - Get current time in any timezone
  - Convert time between timezones
  - Support for IANA timezone names
- ☁️ **AWS Bedrock**: LiteLLM integration with AWS Bedrock Claude model
- 🎯 **Custom Prompts**: Professional prompt templates with tool examples
- 📝 **Template System**: Jinja2-based template rendering for dynamic prompts
- 🔌 **MCP Integration**: Model Context Protocol for Excel and Time server communication
- 🚀 **Natural Language**: Handles complex requests through conversational interface


## Prerequisites

- Python 3.8+
- AWS credentials configured (for Bedrock access)
- AWS region with Bedrock Claude access

## Quick Start

### 1. Setup Environment

```bash
python3 -m venv env
source env/bin/activate
export PYTHONPATH=".:$PYTHONPATH"
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
source env/bin/activate

# Install packages
pip install --index-url https://pypi.org/simple/ -r requirements.txt

# Run the simple agent
python main.py
```

## Usage

### Basic Usage

The agent can handle natural language questions for math, Excel, and time operations:

**Mathematics:**
- "What is 15 + 25?"
- "Can you multiply 7 by 8?"
- "What's 100 divided by 4?"
- "Calculate 50 minus 17"

**Excel Operations:**
- "Create an Excel file with my budget data"
- "Read the sales data from my Excel file"
- "Add a chart to my spreadsheet"

**Time Operations:**
- "What is the current time in UTC?"
- "Convert 2:30 PM New York time to Tokyo time"
- "What time is it in London right now?"

### Programmatic Usage

You can also import and use the agent in your own code:

```python
from agent import SimpleAgent

# Initialize agent
agent = SimpleAgent()

# Ask a question (math, Excel, or time)
response = agent.run("What is 20 + 15?")
print(response)  # Output: 35

response = agent.run("What time is it in Tokyo?")
print(response)  # Output: Current time in Tokyo

response = agent.run("Create an Excel file with my data")
print(response)  # Output: Excel file created successfully
```

## Architecture

The agent follows a modular architecture with MCP server integration:

```
┌─────────────────────────────────────────────────────────────┐
│                     SmolAgent Framework                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ CalculatorTool  │  │  ExcelMCPTool   │  │ TimeMCPTool  │ │
│  │   (Built-in)    │  │                 │  │              │ │
│  └─────────────────┘  └─────────┬───────┘  └──────┬───────┘ │
└──────────────────────────────────┼────────────────┼─────────┘
                                   │                │
                         ┌─────────▼────────────────▼─────────┐
                         │        MCP Connector              │
                         │   (Process Management & I/O)      │
                         └─────────┬────────────────┬─────────┘
                                   │                │
                    ┌──────────────▼──────────────┐ │
                    │    Excel MCP Server         │ │
                    │  (uvx excel-mcp-server)     │ │
                    │                             │ │
                    │ ┌─────────────────────────┐ │ │
                    │ │ • create_workbook       │ │ │
                    │ │ • read_data_from_excel  │ │ │
                    │ │ • write_data_to_excel   │ │ │
                    │ │ • format_cells          │ │ │
                    │ │ • create_chart          │ │ │
                    │ │ • create_pivot_table    │ │ │
                    │ └─────────────────────────┘ │ │
                    └─────────────────────────────┘ │
                                                    │
                                   ┌────────────────▼──────────────┐
                                   │      Time MCP Server          │
                                   │   (uvx mcp-server-time)       │
                                   │                               │
                                   │ ┌───────────────────────────┐ │
                                   │ │ • get_current_time        │ │
                                   │ │ • convert_time            │ │
                                   │ │ • timezone support        │ │
                                   │ └───────────────────────────┘ │
                                   └───────────────────────────────┘

Communication Flow:
1. User asks natural language question
2. SmolAgent processes and determines which tool(s) to use
3. Tool communicates with MCP Server via JSON-RPC over stdin/stdout
4. MCP Server executes operation and returns result
5. Tool formats result for SmolAgent
6. SmolAgent provides natural language response to user
```

### File Organization:

- **main.py**: Entry point with test examples and main function
- **agent.py**: Core agent implementation with `SimpleAgent` and `LiteLLMModel` classes
- **agent_tools/calculator.py**: Modular calculator tool implementation
- **agent_tools/excel_mcp.py**: Excel MCP tool for spreadsheet operations
- **agent_tools/time_mcp.py**: Time MCP tool for date/time operations
- **mcp/connector.py**: MCP connector for managing multiple MCP servers
- **mcp/mcp_servers.json**: Configuration for MCP servers (Excel and Time)
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
│   ├── calculator.py          # Calculator tool implementation
│   ├── excel_mcp.py          # Excel MCP tool
│   └── time_mcp.py           # Time MCP tool
├── mcp/
│   ├── __init__.py
│   ├── connector.py          # MCP connector implementation
│   └── mcp_servers.json      # MCP server configurations
├── prompts/
│   ├── __init__.py
│   └── templates.py           # Professional prompt templates
├── scripts/
│   ├── mcp_demo.py           # MCP demonstration script
│   └── test_excel_agent.py   # Excel agent testing
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
- **CalculatorTool**: Mathematical operations tool following SmolAgent patterns
- **ExcelMCPTool**: Excel operations via MCP server integration
- **TimeMCPTool**: Date/time operations via MCP server integration
- **MCPConnector**: Manages multiple MCP servers (Excel and Time)
- **Template Rendering**: Dynamic prompt generation based on available tools

## Dependencies

- `litellm`: LLM gateway for AWS Bedrock integration
- `smolagents`: Agent framework (v1.17.0 - matches enterprise template)
- `boto3`: AWS SDK for Python
- `jinja2`: Template engine for dynamic prompt generation

## MCP Server Dependencies

The project uses the following MCP servers via uvx (automatically managed):
- `excel-mcp-server`: Excel operations server
- `mcp-server-time`: Time and timezone operations server

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

The project includes MCP connectors for Excel and Time operations:

```bash
# Run main demo with all tools
python main.py

# Run MCP demonstration
python scripts/mcp_demo.py

# Interactive MCP demo
python scripts/mcp_demo.py --interactive
```

**Available MCP Servers:**
- **Excel MCP Server**: Excel file operations (create, read, write), chart and pivot table generation, cell formatting and styling
- **Time MCP Server**: Current time retrieval, timezone conversions, IANA timezone support

**MCP Configuration:**
- Server configurations are defined in `mcp/mcp_servers.json`
- Servers are automatically started via uvx when first used
- Multiple servers can run concurrently
- Each tool manages its own server lifecycle
