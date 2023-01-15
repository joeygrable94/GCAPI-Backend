import time
from typing import Any

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.templates import static_files


def configure_exceptions(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Internal server error",
                headers={
                    "x-request-id": correlation_id.get() or "",
                    "Access-Control-Expose-Headers": "x-request-id",
                },
            ),
        )


def configure_routers(app: FastAPI) -> None:
    from app.api.v1 import router_v1

    app.include_router(router_v1, prefix=f"{settings.API_PREFIX_V1}")


def configure_static(app: FastAPI) -> None:
    app.mount("/static", static_files, name="static")


def configure_events(app: FastAPI) -> None:
    # from app.db.commands import check_db_connected, check_db_disconnected

    # startup actions
    # @app.on_event("startup")
    # async def on_startup() -> None:
    #     await check_db_connected()
    #     await build_database()

    # middlewares
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Any) -> None:
        start_time: Any = time.perf_counter()
        response: Any = await call_next(request)
        process_time: Any = time.perf_counter() - start_time
        response.headers["x-process-time"] = str(process_time)
        return response

    # shutdown actions
    # @app.on_event("shutdown")
    # async def on_shutdown() -> None:
    #     await check_db_disconnected()


def create_app() -> FastAPI:
    # INIT APP
    app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        openapi_url="/api/v1/docs/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
    )
    # MW: logger request process id correlation
    app.add_middleware(CorrelationIdMiddleware)
    # MW: Cross-Origin Resource Sharing protection
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(  # pragma: no cover
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )
    configure_exceptions(app)
    configure_routers(app)
    configure_static(app)
    configure_events(app)
    return app


app: FastAPI = create_app()
