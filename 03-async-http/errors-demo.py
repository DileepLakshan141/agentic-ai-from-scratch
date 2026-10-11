import os
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, AuthenticationError

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"), base_url="http://localhost:9999", timeout=10
)

try:
    resonse = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=10,
    )
except AuthenticationError as exc:
    print(f"Auth error: status:{exc.status_code}")
except APIConnectionError as exc:
    print(f"Cannot reach the servers:{type(exc).__name__}")
