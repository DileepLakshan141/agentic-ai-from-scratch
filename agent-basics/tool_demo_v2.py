import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

PRICES = {"keyboard": 9500, "mouse": 650, "speakers": 1400}

messages = [
    {
        "role": "user",
        "content": "Give me the total price of a keyboard, a mouse and speakers?",
    }
]

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

MAX_STEPS = 5

client = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))

for step in range(1, MAX_STEPS + 1):
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"), messages=messages, tools=tools
    )
    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        print("FINAL: ", message.content)
        break

    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        result = PRICES.get(args["item"])
        print(f"step: {step} , {call.function.name}({args}) -> {result}")
        messages.append(
            {"role": "tool", "tool_call_id": call.id, "content": str(result)}
        )
else:
    print("stopped: MAX_STEPS reached")
