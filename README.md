# Simple Agent with Calculator Tool

A minimal implementation of an AI agent using SmolAgent with LiteLLM via AWS Bedrock and a simple calculator tool.

## Features

- 🤖 **SmolAgent**: Uses the SmolAgent framework for agent functionality
- 🔢 **Calculator Tool**: Simple arithmetic operations (add, subtract, multiply, divide)  
- ☁️ **AWS Bedrock**: LiteLLM integration with AWS Bedrock Claude model
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
python simple_agent.py
```

## Usage

The agent can handle natural language math questions:

- "What is 15 + 25?"
- "Can you multiply 7 by 8?"
- "What's 100 divided by 4?"
- "Calculate 50 minus 17"

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
test-mcp-connector/
├── simple_agent.py      # Main agent implementation
├── requirements.txt     # Python dependencies  
├── setup.sh            # Setup script
├── README.md           # This file
└── venv/               # Virtual environment (created by setup)
```

## Dependencies

- `litellm`: LLM gateway for AWS Bedrock integration
- `smolagents`: Agent framework
- `boto3`: AWS SDK for Python

## Troubleshooting

### AWS Bedrock Access
- Ensure you have access to Claude models in your AWS region
- Check that your IAM user/role has Bedrock permissions
- Verify the model ID is correct for your region

### Environment Issues
- Make sure virtual environment is activated
- Check Python version (3.8+ required)
- Reinstall dependencies if needed: `pip install -r requirements.txt`
