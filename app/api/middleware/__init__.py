import time
from typing import Any, List

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request
from fastapi_profiler import PyInstrumentProfilerMiddleware  # type: ignore
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.deps.get_client_ip import get_request_client_ip
from app.core.config import settings


def configure_middleware(app: FastAPI) -> None:
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(
        PyInstrumentProfilerMiddleware,
        # Required to output the profile on server shutdown
        server_app=app,
        profiler_output_type="html",
        # Set to True to show request profile on stdout on each request
        is_print_each_request=False,
        # Set to true to open your web-browser automatically
        # when the server shuts down
        open_in_browser=False,
        # Filename for output
        html_file_name=f"{settings.api.key}_profile.html",
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.api.session_secret_key,
        session_cookie="gcapi_session",
    )
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
    #     print(f"Request from IP: {req_ip}")
    #     response_result: Any = await call_next(request)
    #     print('response_result', response_result)
    #     return response_result


__all__: List[str] = [
    "configure_middleware",
]
