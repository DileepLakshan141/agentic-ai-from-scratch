from typing import Protocol


class LLMClient(Protocol):
    def complete(self, prompt: str):
        """Send a prompt and return the model's text reply."""
