import os

from dotenv import load_dotenv
from openai import OpenAI


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"{name} is not set in .env")
    return value


def build_client() -> OpenAI:
    load_dotenv()
    return OpenAI(
        api_key=get_env("LLM_API_KEY"),
        base_url=get_env("LLM_BASE_URL"),
        timeout=30,
    )


def llm(prompt: str, client: OpenAI | None = None) -> str:
    if client is None:
        client = build_client()
    response = client.chat.completions.create(
        model=get_env("LLM_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("The model returned an empty response")
    return content
