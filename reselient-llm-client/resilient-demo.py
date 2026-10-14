import time
import random
from RateLimit import RateLimitError

state = {"calls": 0}


def caller() -> str:
    state["calls"] += 1
    if state["calls"] < 3:
        raise RateLimitError(retry_after=3.0)
    return "connected succesfully!"


def backoff_delay(attempt: int, base: float = 0.5, cap: float = 1.0) -> float:
    delay = min(cap, base * 2 ** (attempt - 1))
    return delay


def call_with_retries(max_attempts: int = 5) -> str:
    for attempt in range(1, max_attempts + 1):
        try:
            return caller()
        except (ConnectionError, RateLimitError) as exc:
            print(f"attempt {attempt} failed: {exc}")
            if attempt == max_attempts:
                raise
            if isinstance(exc, RateLimitError) and exc.retry_after is not None:
                delay = exc.retry_after
            else:
                delay = backoff_delay(attempt)
            print(f"waiting {delay:.2f}s")
            time.sleep(delay)

    raise RuntimeError("unreachable!")


print(call_with_retries(10))
