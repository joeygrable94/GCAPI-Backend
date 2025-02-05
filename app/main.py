from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sentry_sdk import Client

from app.api.exceptions import configure_exceptions
from app.api.middleware import configure_middleware
from app.config import settings
from app.core.templates import static_files
from app.db.commands import check_db_connected, check_db_disconnected
from app.services.csrf import CsrfProtect, CsrfSettings
from app.services.sentry import configure_sentry_monitoring
from app.utilities.route_map import make_routes_map

if settings.api.mode == "production":  # pragma: no cover
    sentry_client: Client | None = configure_sentry_monitoring() 


@asynccontextmanager
async def application_lifespan(app: FastAPI) -> AsyncGenerator:  # pragma: no cover
    await check_db_connected()

    @CsrfProtect.load_config
    def get_csrf_config() -> CsrfSettings:
        return CsrfSettings()

    yield
    await check_db_disconnected()


def configure_routers(app: FastAPI) -> None:
    from app.api.endpoints_v1 import router_v1

    app.include_router(router_v1, prefix=settings.api.prefix)
    make_routes_map(app)


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
    configure_static(app)
    configure_routers(app)
    return app


app: FastAPI = create_app()
