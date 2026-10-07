class HFHelloError(Exception):
    """Base class for all application errors."""


class ConfigError(HFHelloError):
    """Missing or invalid configuration."""


class InvalidPromptError(HFHelloError):
    """The user supplied an unusable prompt."""


class LLMError(HFHelloError):
    """The LLM provider call failed."""
