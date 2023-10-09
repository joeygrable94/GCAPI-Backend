import time
from typing import Any

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from starlette.middleware.sessions import SessionMiddleware

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.schemas import RateLimitedToken

from .rate_limiter import limiter
from .utilities import get_request_client_ip


def configure_middleware(app: FastAPI) -> None:
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Any) -> Any:
        """Adds a header to each response with the time it took to process."""
        start_time: Any = time.perf_counter()
        response_result: Any = await call_next(request)
        process_time: Any = time.perf_counter() - start_time
        response_result.headers["X-PROCESS-TIME"] = str(process_time)
        return response_result

    @app.middleware("http")
    async def add_global_request_rate_limit(request: Request, call_next: Any) -> Any:
        """
        Manages a request token for each ip address and limits the number
        of requests per second.
        """
        client_ip = get_request_client_ip(request)
        ip_limit: RateLimitedToken = await limiter(client_ip, 100, 60)

        if not ip_limit.call:
            return await http_exception_handler(
                request,
                HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "message": ErrorCode.IP_RESTRICTED_TOO_MANY_REQUESTS,
                        "ttl": ip_limit.ttl,
                    },
                ),
            )

        return await call_next(request)


__all__ = [
    "configure_middleware",
    "limiter",
    "get_request_client_ip",
]
