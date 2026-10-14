import openai
import os
import random
import time
from collections.abc import Callable
from dotenv import load_dotenv

RETRYABLE = (
    openai.RateLimitError,
    openai.APIConnectionError,
    openai.APITimeoutError,
    openai.InternalServerError,
)


def backoff_delay(attempt: int, base: float = 0.5, cap: float = 8.0) -> float:
    return random.uniform(0, min(cap, base * 2 ** (attempt - 1)))


def with_retries(
    fn: Callable[[], str],
    max_attempts: int = 5,
    sleep: Callable[[float], None] = time.sleep,
):
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except RETRYABLE:
            if attempt == max_attempts:
                raise
            sleep(backoff_delay(attempt))

    return RuntimeError("max attempts >= 1")
