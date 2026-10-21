import json
import os
import typing
from collections.abc import Callable

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionFunctionToolParam

from file_tools import read_file, write_file

MAX_STEPS = 5
load_dotenv()

MESSAGES: list[typing.Any] = [
    {
        "role": "system",
        "content": "You are a coding assistant. Use read_file to read files and write_file to write into the file. "
        "Only describe what the file really contains; never guess.",
    },
    {
        "role": "user",
        "content": "Write the text 'hello' to ../evil.txt",
    },
]


TOOLS: list[ChatCompletionFunctionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file from the project sandbox folder",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "file name, e.g. calc.py"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a file in the sandbox. Replaces the whole file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "file name, e.g. calc.py",
                    },
                    "content": {
                        "type": "string",
                        "description": "the complete new file content",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
]


TOOL_FUNCTIONS: dict[str, Callable[..., str]] = {
    "read_file": read_file,
    "write_file": write_file,
}


def run_tool(tool_name: str, raw_args: str) -> str:
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return (
            f"ERROR: unknown tool '{tool_name}'. Available: {', '.join(TOOL_FUNCTIONS)}"
        )
    try:
        args = json.loads(raw_args)
        return func(**args)
    except (json.JSONDecodeError, TypeError) as exc:
        return f"ERROR: bad arguments ({exc})"


client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])

for step in range(1, MAX_STEPS + 1):
    response = client.chat.completions.create(
        model=os.environ["LLM_MODEL"], messages=MESSAGES, tools=TOOLS
    )
    message = response.choices[0].message
    MESSAGES.append(message)

    if not message.tool_calls:
        print("FINAL:", message.content)
        break
    for call in message.tool_calls:
        if call.type != "function":
            MESSAGES.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": "ERROR: unsupported",
                }
            )
            continue
        result = run_tool(call.function.name, call.function.arguments)
        print(f"step {step}: {call.function.name}({call.function.arguments})")
        MESSAGES.append({"role": "tool", "tool_call_id": call.id, "content": result})
else:
    print("stopped: MAX_STEPS reached")
