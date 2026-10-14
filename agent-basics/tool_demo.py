import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PRICES = {"keyboard": 8500, "mouse": 3200}

client = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "Get the price in LKR of an item sold in our shop",
            "parameters": {
                "type": "object",
                "properties": {"item": {"type": "string"}},
                "required": ["item"],
            },
        },
    }
]

response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL"),
    messages=[
        {"role": "user", "content": "How much does a keyboard cost in our shop?"}
    ],
    tools=tools,
)
message = response.choices[0].message
print("Content: ", message.content)
print("Tool Calls: ", message.tool_calls)

if message.tool_calls:
    call = message.tool_calls[0]
    args = json.loads(call.function.arguments)
    print(call.function.name, args, "->", PRICES.get(args["item"]))
