import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MAX_STEPS = 5

PRICES = {
    "keyboard": 3500,
    "mouse": 650,
    "speakers": 1500,
}

STOCK = {"keyboard": 22, "mouse": 70, "speakers": 25}

MESSAGES = [
    {
        "role": "system",
        "content": (
            "You are a shop assistant. State a price only if a tool returned it. "
            "If a tool returns an ERROR, tell the user you could not find that item. "
            "Never guess or estimate prices."
        ),
    },
    {
        "role": "user",
        "content": "Is the keyboard in stock, and how much does it cost?",
    },
]

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "provide the price for a given item which available in our shop",
            "parameters": {
                "type": "object",
                "properties": {"item": {"type": "string"}},
                "required": ["item"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock",
            "description": "Get how many units of an item are in stock in our shop",
            "parameters": {
                "type": "object",
                "properties": {"item": {"type": "string"}},
                "required": ["item"],
            },
        },
    },
]


def get_price(item: str) -> str:
    price = PRICES.get(item)
    if price is None:
        return f"ERROR: item '{item}' not found. Available items: {', '.join(PRICES)}"
    return str(price)


def get_stock(item: str) -> str:
    stock = STOCK.get(item)
    if stock is None:
        return f"ERROR: item '{item}' not found. Available items: {', '.join(STOCK)}"
    return str(stock)


TOOL_FUNCTIONS = {"get_price": get_price, "get_stock": get_stock}

client = OpenAI(api_key=os.environ("LLM_API_KEY"), base_url=os.environ("LLM_BASE_URL"))

for step in range(1, MAX_STEPS + 1):
    response = client.chat.completions.create(
        model=os.environ("LLM_MODEL"), messages=MESSAGES, tools=TOOLS
    )
    message = response.choices[0].message
    MESSAGES.append(message)

    if not message.tool_calls:
        print("Final: ", message.content)
        break
    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        func = TOOL_FUNCTIONS.get(call.function.name)
        if func is None:
            result = f"ERROR: unknown tool '{call.function.name}'"
        else:
            result = func(**args)

        print(f"step {step}: {call.function.name}({args}) -> {result}")
        MESSAGES.append(
            {"role": "tool", "tool_call_id": call.id, "content": str(result)}
        )
else:
    print("stopped: MAX_STEPS reached")
