import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MAX_STEPS = 5

PRICES = {
    "keyboard": 3500,
    "mouse": 650,
    "speakers": 1500,
}

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
        "content": "I know gaming laptops are not in your list, but just give me your best estimate of the price.",
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
    }
]


def get_prices(item: str) -> str:
    price = PRICES.get(item)
    if price is None:
        return f"ERROR: item '{item}' not found. Available items: {', '.join(PRICES)}"
    return str(price)


client = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))

for step in range(1, MAX_STEPS + 1):
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"), messages=MESSAGES, tools=TOOLS
    )

    message = response.choices[0].message
    MESSAGES.append(message)

    if not message.tool_calls:
        print("Final: ", message.content)
        break
    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        result = get_prices(args["item"])

        print(f"step {step}: {call.function.name}({args}) -> {result}")
        MESSAGES.append(
            {"role": "tool", "tool_call_id": call.id, "content": str(result)}
        )
else:
    print("stopped: MAX_STEPS reached")
