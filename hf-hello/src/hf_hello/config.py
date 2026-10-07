import os
from dataclasses import field, dataclass
from typing import Self
from dotenv import load_dotenv
from hf_hello.exceptions import ConfigError


@dataclass(frozen=True, slots=True)
class Settings:
    """Immutable, typed application settings."""

    hf_token: str = field(repr=False)
    hf_model: str
    request_timeout_s: float = 30.0
    max_tokens: int = 256
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> Self:
        load_dotenv()

        token = os.getenv("HF_TOKEN", "").strip()
        model = os.getenv("HF_MODEL", "").strip()
        hf_credentials = (("HF_TOKEN", token), ("HF_MODEL", model))

        missing = [name for name, value in hf_credentials if not value]

        if missing:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        try:
            timeout = float(os.getenv("REQUEST_TIMEOUT_S", "30"))
            max_tokens = int(os.getenv("MAX_TOKENS", "256"))
        except ValueError as exec:
            raise ConfigError(
                "REQUEST_TIMEOUT_S must be a number and MAX_TOKENS must be an integer"
            ) from exec

        return cls(
            hf_token=token,
            hf_model=model,
            request_timeout_s=timeout,
            max_tokens=max_tokens,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )
