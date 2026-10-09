from unittest.mock import MagicMock

import pytest
from groq_llm_v2 import llm


def make_fake_client(reply: str | None) -> MagicMock:
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=reply))
    ]
    return fake_client


def test_llm_returns_model_text() -> None:
    fake_client = make_fake_client("Hi there")

    result = llm("hello", client=fake_client)

    assert result == "Hi there"

    call_kwargs = fake_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["messages"][0]["content"] == "hello"


def test_llm_raises_on_empty_response() -> None:
    fake_client = make_fake_client(None)

    with pytest.raises(ValueError):
        llm("hello", client=fake_client)
