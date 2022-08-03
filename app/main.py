import time
from typing import Any

from fastapi import FastAPI
from requests import Request
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.templates import static_files


def configure_routers(app: FastAPI) -> None:
    from app.api.v1 import router_v1

    app.include_router(router_v1, prefix=f"{settings.API_PREFIX_V1}")


def configure_static(app: FastAPI) -> None:
    app.mount("/static", static_files, name="static")


def configure_events(app: FastAPI) -> None:
    from app.db.commands import (
        check_db_connected,
        check_db_disconnected,
        create_initial_data,
    )

    # startup actions
    @app.on_event("startup")
    async def on_startup() -> None:
        await check_db_connected()
        await create_initial_data()

    # middlewares
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Any) -> None:
        start_time: Any = time.perf_counter()
        response: Any = await call_next(request)
        process_time: Any = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # shutdown actions
    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await check_db_disconnected()


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        openapi_url="/api/v1/docs/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
    )
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )
    configure_routers(app)
    configure_static(app)
    configure_events(app)
    return app


app: FastAPI = create_app()
