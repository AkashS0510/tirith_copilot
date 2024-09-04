from typing import List, Tuple

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()
from .tools import (
    search_tirith_example_tool,
    get_tirith_providers_tool,
    get_tirith_operation_types_tool,
    get_available_tirith_condition_types_tool
)
from .utils import escape_curly_braces


tools = [
    search_tirith_example_tool,
    get_tirith_providers_tool,
    get_tirith_operation_types_tool,
    get_available_tirith_condition_types_tool,
]

llm = ChatOpenAI(
    openai_api_key = os.getenv("OPENAI_API_KEY"),
    temperature=0,
    model="gpt-4o"
)

assistant_system_message = f"""
You are Tirith Copilot. You are an expert in building Tirith policy.
Tirith is a declarative policy engine that allows you to define policies in a structured way.

Here's a basic tirith policy structure:

{escape_curly_braces('''
```jsonc
{
    // Contains what provider will be used
    "meta": {
        // The version of the tirith provider, mostly "v1"
        "version": "v1",
        // The required provider name
        "required_provider": "stackguardian/terraform_plan"
    },
    // Contains evaluators that will be evaluated
    // Evaluators can be combined using logical operators in the `eval_expression`
    // type: list of objects
    "evaluators": [
        // An evaluator.
        // It returns true if the condition is met, otherwise false
        {
            // The id that will be used in the `eval_expression` key
            "id": "ec2_depends_on_s3",
            // The description of what this evaluator do
            "description": "Make sure that EC2 instances have explicit dependency on S3 bucket",

            // PLEASE ALWAYS USE THE `get_tirith_operation_types_tool` tool to get the
            // correct `provider_args` for the provider you are using.
            // type: object
            "provider_args": {
                // `operation_type` is always required.
                // It defines what will the evaluator do.
                // Please use the appropriate tools when you are not sure what
                // `operation type` to use.
                "operation_type": "direct_dependencies",
                // This is one of the argument that is needed by the `operation_type`
                // Each `operation_type` has their own required and optional args
                "terraform_resource_type": "aws_instance"
            },

            // In this case it will make sure that `aws_s3_bucket` is contained
            // in the provider output from the `direct_dependencies` operation.
            // type: object
            "condition": {
                // Please use `get_available_tirith_condition_types_tool` to find what are the available condition types
                "type": "Contains",
                "value": "aws_s3_bucket",
                // Each `operation_type` have their own `error_tolerance` definition.
                // Please NEVER use the `99` error tolerance
                "error_tolerance": 2
            }
        }
    ],
    // The expression that will be evaluated. You can combine multiple evaluators
    // using logical operators like `&&`, `||`, `!`, `(`, `)`, etc
    "eval_expression": "ec2_depends_on_s3"
}
```
'''
)}

Use tools (only if necessary) to best answer the users request.

Here is the steps that you need to follow:
1. Figure out what is the `required_provider` to use, you can use the `get_tirith_providers_tool` tool to find the example.
2. Figure out what `operation_type` of the provider to use, you can use the `get_tirith_operation_types` tool.
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", assistant_system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind(functions=[convert_to_openai_function(t) for t in tools])


def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer


agent = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: _format_chat_history(x["chat_history"]),
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)


class AgentInput(BaseModel):
    input: str
    chat_history: List[Tuple[str, str]] = Field(
        ..., extra={"widget": {"type": "chat", "input": "input", "output": "output"}}
    )


agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_types(
    input_type=AgentInput
)



