import json
import os
import typing

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionFunctionToolParam

from file_tools import read_file

load_dotenv()

MAX_STEPS = 5

messages: list[typing.Any] = [
    {
        "role": "system",
        "content": "You are a coding assistant. Use read_file to read files. "
        "Only describe what the file really contains; never guess.",
    },
    {"role": "user", "content": "Read calc.py and tell me if add() has a bug."},
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
    }
]


def run_tool(name: str, raw_arguments: str) -> str:
    if name != "read_file":
        return f"ERROR: unknown tool '{name}'"
    try:
        args = json.loads(raw_arguments)
        return read_file(args["path"])
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        return f"ERROR: bad arguments ({exc})"


client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])

for step in range(1, MAX_STEPS + 1):
    response = client.chat.completions.create(
        model=os.environ["LLM_MODEL"], messages=messages, tools=TOOLS
    )
    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        print("FINAL:", message.content)
        break

    for call in message.tool_calls:
        if call.type != "function":
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": "ERROR: unsupported",
                }
            )
            continue
        result = run_tool(call.function.name, call.function.arguments)
        print(f"step {step}: {call.function.name}({call.function.arguments})")
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
else:
    print("stopped: MAX_STEPS reached")
