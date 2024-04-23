import time
from typing import Any, List

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.deps import get_request_client_ip
from app.api.deps.get_auth import get_current_user
from app.core import logger
from app.core.config import settings


def configure_middleware(app: FastAPI) -> None:
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=settings.api.secret_key)
    if settings.api.allowed_cors:
        app.add_middleware(  # pragma: no cover
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.api.allowed_cors],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Any) -> Any:
        """Adds a header to each response with the time it took to process."""
        start_time: Any = time.perf_counter()
        response_result: Any = await call_next(request)
        process_time: Any = time.perf_counter() - start_time
        response_result.headers["X-Process-Time"] = str(process_time)
        return response_result

    # @app.middleware("http")
    # async def log_ip_activity(request: Request, call_next: Any) -> Any:
    #     """Adds a header to each response with the time it took to process."""
    #     req_ip = get_request_client_ip(request)
    #     response_result: Any = await call_next(request)
    #     return response_result


__all__: List[str] = [
    "configure_middleware",
]
