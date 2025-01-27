from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sentry_sdk import Client

from app.api.exceptions import configure_exceptions
from app.api.middleware import configure_middleware
from app.api.monitoring import configure_monitoring
from app.core.config import settings
from app.core.security import (
    CsrfProtect,
    CsrfSettings,
    configure_authorization_exceptions,
    configure_csrf_exceptions,
    configure_encryption_exceptions,
    configure_permissions_exceptions,
)
from app.core.templates import static_files
from app.db.commands import check_db_connected, check_db_disconnected

sentry_client: Client | None = configure_monitoring()


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncGenerator:  # pragma: no cover
    # startup
    await check_db_connected()

    @CsrfProtect.load_config
    def get_csrf_config() -> CsrfSettings:
        return CsrfSettings()

    yield

    # shutdown
    await check_db_disconnected()


def configure_routers(app: FastAPI) -> None:
    from app.api.v1 import router_v1

    app.include_router(router_v1, prefix=settings.api.prefix)

    # endpoints = []
    # for route in app.routes:
    #     if isinstance(route, APIRoute):
    #         endpoints.append(route.path)
    # with open("docs/endpoints.txt", "w") as f:
    #     f.write("\n".join(endpoints))


def configure_static(app: FastAPI) -> None:
    app.mount("/static", static_files, name="static")


def create_app() -> FastAPI:
    deps: list = []
    app: FastAPI = FastAPI(
        title=settings.api.name,
        version=settings.api.version,
        openapi_url="/api/docs/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        dependencies=[Depends(dep) for dep in deps],
        lifespan=application_lifespan,
    )
    configure_middleware(app)
    configure_exceptions(app)
    configure_permissions_exceptions(app)
    configure_authorization_exceptions(app)
    configure_csrf_exceptions(app)
    configure_encryption_exceptions(app)
    configure_static(app)
    configure_routers(app)
    return app


app: FastAPI = create_app()
