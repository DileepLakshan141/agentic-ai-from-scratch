class RateLimitError(Exception):
    def __init__(self, retry_after: None = None):
        super().__init__("rate limited")
        self.retry_after = retry_after
