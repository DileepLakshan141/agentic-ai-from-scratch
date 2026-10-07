import logging
import sys


def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stderr,
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
