import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")
    if api_key is None or base_url is None or model is None:
        raise ValueError("LLM_API_KEY, LLM_BASE_URL and LLM_MODEL must be set in .env")

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=80)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "what is the capital of Sri Lanka."}],
        max_tokens=100,
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
