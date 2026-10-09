import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_env(prop: str) -> str:
    property = os.getenv(prop)
    if property is None:
        raise ValueError(f"property {prop} can not be empty!")
    return property


def llm(prompt: str) -> str:
    client = OpenAI(api_key=get_env("LLM_API_KEY"), base_url=get_env("LLM_BASE_URL"), timeout=60)
    response = client.chat.completions.create(
        model=get_env("LLM_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )

    content = response.choices[0].message.content
    if content is None:
        raise ValueError("LLM returned empty response!")

    return content
