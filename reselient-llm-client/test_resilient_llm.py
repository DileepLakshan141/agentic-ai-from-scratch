from unittest.mock import MagicMock

import httpx
import openai

from resilient_llm import with_retries


def make_error() -> openai.APIConnectionError:
    return openai.APIConnectionError(request=httpx.Request("POST", "http://test"))


def test_retries_then_succeeds() -> None:
    fn = MagicMock(side_effect=[make_error(), make_error(), "ok"])
    sleeps: list[float] = []
    assert with_retries(fn, sleep=sleeps.append) == "ok"
    assert fn.call_count == 3
    assert len(sleeps) == 2
