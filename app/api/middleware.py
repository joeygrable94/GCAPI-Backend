import time
from typing import Any

from fastapi import FastAPI, Request
from fastapi_profiler import PyInstrumentProfilerMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.entities.ipaddress.dependencies import get_request_ip


def configure_middleware(app: FastAPI) -> None:
    app.add_middleware(
        PyInstrumentProfilerMiddleware,
        server_app=app.router,
        profiler_output_type="html",
        is_print_each_request=False,
        open_in_browser=False,
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
    async def add_process_time_header(
        request: Request, call_next: Any
    ) -> Any:  # pragma: no cover
        """Adds a header to each response with the time it took to process."""
        start_time: Any = time.perf_counter()
        response_result: Any = await call_next(request)
        process_time: Any = time.perf_counter() - start_time
        response_result.headers["x-process-time"] = str(process_time)
        return response_result

    @app.middleware("http")
    async def add_reques_ip_header(
        request: Request, call_next: Any
    ) -> Any:  # pragma: no cover
        """Adds a header to each response with the time it took to process."""
        req_ip = get_request_ip(request)
        response_result: Any = await call_next(request)
        response_result.headers["x-request-ip"] = str(req_ip)
        return response_result


__all__: list[str] = [
    "configure_middleware",
]
