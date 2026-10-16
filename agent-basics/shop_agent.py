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

MESSAGES: list[any] = [
    {
        "role": "system",
        "content": (
            "You are a shop assistant. State a price only if a tool returned it. "
            "If a tool returns an ERROR, tell the user you could not find that item. "
            "Never guess or estimate prices."
            "All the prices are in LKR."
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
        return f"price is not available for that item! available items: {', '.join(PRICES)}"
    return str(price)


def get_stock(item: str) -> str:
    stock = STOCK.get(item)
    if stock is None:
        return (
            f"stock is not available for that item! available items: {', '.join(STOCK)}"
        )
    return str(stock)


TOOL_FUNCTIONS = {"get_price": get_price, "get_stock": get_stock}


def run_tool(name: str, raw_arguments: str) -> str:
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return f"ERROR: unknown tool '{name}'. Available tools: {', '.join(TOOL_FUNCTIONS)}"
    try:
        args = json.loads(raw_arguments)
    except json.JSONDecodeError as exc:
        return f"ERROR: arguments are not valid JSON ({exc})"
    if not isinstance(args, dict):
        return "ERROR: arguments must be a JSON object"
    try:
        return func(**args)
    except TypeError as exc:
        return f"ERROR: wrong arguments for '{name}': {exc}"


client = OpenAI(api_key=os.environ("LLM_API_KEY"), base_url=os.environ("LLM_BASE_URL"))

for step in range(1, MAX_STEPS + 1):
    response = client.chat.completions.create(
        model=os.environ("LLM_MODEL"), messages=MESSAGES, tools=TOOLS
    )
    message = response.choices[0].message
    MESSAGES.append(message)

    if not message.tool_calls:
        print("FINAL: ", message.content)
        break
    for call in message.tool_calls:
        result = run_tool(call.function.name, call.function.arguments)
        print(
            f"step {step}: {call.function.name}({call.function.arguments}) -> {result}"
        )
        MESSAGES.append({"role": "tool", "tool_call_id": call.id, "content": result})
else:
    print("stopped: MAX_STEPS reached")
