import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def greet(name: str, greeting: str) -> str:
    return f"{greeting}, {name}!"


def main() -> None:
    load_dotenv()
    name = os.getenv("GREETING_NAME")
    if name is None:
        raise ValueError("GREETING_NAME is not set in .env")
    logger.info("Greeting user")
    print(greet(name, "Good Morning"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")
    try:
        main()
        logger.debug("name loaded")
    except ValueError as exc:
        logger.error("Startup failed: %s", exc)
