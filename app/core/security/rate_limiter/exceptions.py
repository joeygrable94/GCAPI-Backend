from typing import Dict

from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler


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


def configure_rate_limiter_exceptions(app: FastAPI) -> None:

    @app.exception_handler(RateLimitedRequestException)
    async def rate_limited_request_exception_handler(
        request: Request, exc: RateLimitedRequestException
    ) -> Response:  # noqa: E501
        request_headers = {
            "x-request-id": correlation_id.get() or "",
            "Access-Control-Expose-Headers": "x-request-id",
        }
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers=request_headers,
            ),
        )
