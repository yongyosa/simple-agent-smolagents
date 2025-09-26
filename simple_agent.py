#!/usr/bin/env python3

"""
Simple Agent with SmolAgent, LiteLLM via AWS Bedrock, and Calculator Tool
"""

import litellm
from jinja2 import Template
from typing import Dict, List, Optional, Union
from smolagents import CodeAgent, Tool, Model, ChatMessage, MessageRole, TokenUsage

from prompts.templates import (
    action_planning_template,
    tool_description_template,
    SMOLAGENT_PLANNING_INITIAL_TEMPLATE,
    SMOLAGENT_PLANNING_UPDATE_PRE_TEMPLATE,
    SMOLAGENT_PLANNING_UPDATE_POST_TEMPLATE,
    SMOLAGENT_MANAGED_AGENT_TASK_TEMPLATE,
    SMOLAGENT_MANAGED_AGENT_REPORT_TEMPLATE,
    SMOLAGENT_FINAL_ANSWER_PRE_TEMPLATE,
    SMOLAGENT_FINAL_ANSWER_POST_TEMPLATE,
)


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


class LiteLLMModel(Model):
    """This model connects to LiteLLM as a gateway to hundreds of LLMs."""

    def __init__(
        self,
        model_id="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        aws_region_name="us-east-1",
        api_base=None,
        api_key=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.aws_region_name = aws_region_name
        # IMPORTANT - Set this to TRUE to add the function to the prompt for Non OpenAI LLMs
        litellm.add_function_to_prompt = True
        self.api_base = api_base
        self.api_key = api_key

    def __call__(
        self,
        messages: List[Dict[str, str]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        **kwargs,
    ) -> ChatMessage:
        for item in messages:
            for content_item in item["content"]:
                content_item["text"] = content_item["text"].strip()

        completion_kwargs = self._prepare_completion_kwargs(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            model=self.model_id,
            aws_region_name=self.aws_region_name,
            api_base=self.api_base,
            api_key=self.api_key,
            convert_images_to_image_urls=True,
            **kwargs,
        )

        response = litellm.completion(**completion_kwargs)

        self._last_input_token_count = response.usage.prompt_tokens
        self._last_output_token_count = response.usage.completion_tokens
        message = ChatMessage.from_dict(
            response.choices[0].message.model_dump(
                include={"role", "content", "tool_calls"}
            )
        )
        message.raw = response

        if tools_to_call_from is not None:
            return message.parse_tool_calls()
        return message

    def generate(
        self,
        messages: List[Union[Dict[str, str], ChatMessage]],
        stop_sequences: Optional[List[str]] = None,
        response_format: Optional[Dict[str, str]] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        **kwargs,
    ) -> ChatMessage:
        response = self.__call__(
            messages=messages,
            stop_sequences=stop_sequences,
            tools_to_call_from=tools_to_call_from,
            **kwargs,
        )

        # If self.__call__ returned a dict instead of ChatMessage, convert it
        if isinstance(response, dict):
            return ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response.get("content", ""),
                raw=response,
                token_usage=TokenUsage(input_tokens=0, output_tokens=0),
            )
        
        # Otherwise, return it as-is
        return response


class SimpleAgent:
    """Simple agent with calculator tool and AWS Bedrock LLM."""

    def __init__(
        self,
        model_id: str = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        aws_region_name: str = "us-east-1",
    ):
        self.model_id = model_id
        self.aws_region_name = aws_region_name
        self.agent = self._init_agent()

    def _init_agent(self) -> CodeAgent:
        """Initialize the CodeAgent with calculator tool and custom prompts."""
        
        # Create tools list
        tools_list = [CalculatorTool()]
        
        # Prepare dynamic values for prompt templates
        tool_descriptions = self._render_tool_descriptions(tools_list)
        authorized_imports = "math, numpy, pandas"  # Basic math imports
        
        # Render the main system prompt
        planning_prompt = (
            action_planning_template.replace("{{tool_descriptions}}", tool_descriptions)
            .replace("{{managed_agents_descriptions}}", "")
            .replace("{{authorized_imports}}", authorized_imports)
        )
        
        # Create agent with LiteLLM model and custom prompt templates
        agent = CodeAgent(
            tools=tools_list,
            model=LiteLLMModel(self.model_id, aws_region_name=self.aws_region_name),
            prompt_templates={
                "system_prompt": planning_prompt,
                "planning": {
                    "initial_plan": SMOLAGENT_PLANNING_INITIAL_TEMPLATE,
                    "update_plan_pre_messages": SMOLAGENT_PLANNING_UPDATE_PRE_TEMPLATE,
                    "update_plan_post_messages": SMOLAGENT_PLANNING_UPDATE_POST_TEMPLATE
                },
                "managed_agent": {
                    "task": SMOLAGENT_MANAGED_AGENT_TASK_TEMPLATE,
                    "report": SMOLAGENT_MANAGED_AGENT_REPORT_TEMPLATE
                },
                "final_answer": {
                    "pre_messages": SMOLAGENT_FINAL_ANSWER_PRE_TEMPLATE,
                    "post_messages": SMOLAGENT_FINAL_ANSWER_POST_TEMPLATE
                },
            },
            additional_authorized_imports=authorized_imports.split(","),
            max_print_outputs_length=200,
        )
        
        return agent

    @staticmethod
    def _render_tool_descriptions(tools_list) -> str:
        """Render tool descriptions using the template."""
        template = Template(tool_description_template)
        return "\n".join(template.render(tool=tool) for tool in tools_list)

    def run(self, question: str) -> str:
        """Run the agent with a question and return the response."""
        try:
            response = self.agent.run(question)
            return str(response)
        except Exception as e:
            return f"Error: {str(e)}"


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
