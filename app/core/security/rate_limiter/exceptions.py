from typing import Dict

from fastapi import status


class RateLimitedRequestException(Exception):
    def __init__(
        self,
        expire: int,
        status_code: int = status.HTTP_429_TOO_MANY_REQUESTS,
        message: str = "Too Many Requests",
    ):
        self.status_code = status_code
        self.message = message
        self.headers: Dict[str, str] = {"Retry-After": str(expire)}
