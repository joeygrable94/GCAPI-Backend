from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import Depends, FastAPI
from sentry_sdk import Client

from app.api.exceptions import configure_exceptions
from app.api.middleware import configure_middleware
from app.api.monitoring import configure_monitoring
from app.core.config import ApiModes, settings
from app.core.redis import redis_conn
from app.core.security import (
    CsrfProtect,
    CsrfSettings,
    FastAPILimiter,
    RateLimiter,
    configure_authorization_exceptions,
    configure_csrf_exceptions,
    configure_encryption_exceptions,
    configure_permissions_exceptions,
    configure_rate_limiter_exceptions,
)
from app.core.templates import static_files
from app.db.commands import (
    check_db_connected,
    check_db_disconnected,
    check_redis_connected,
)

sentry_client: Client | None = configure_monitoring()


@asynccontextmanager  # type: ignore
async def application_lifespan(app: FastAPI) -> AsyncGenerator:
    # application lifespan actions: startup and shutdown
    check_redis_connected()
    # check DB connected
    await check_db_connected()
    # check REDIS connected
    await FastAPILimiter.init(redis_conn, prefix="gcapi-limit")

    # load CSRF settings
    @CsrfProtect.load_config
    def get_csrf_config() -> Any:  # type: ignore
        return CsrfSettings()

    # yeild the application
    yield
    # close REDIS connection
    await FastAPILimiter.close()
    # close DB connection
    await check_db_disconnected()


def configure_routers(app: FastAPI) -> None:
    from app.api.v1 import router_v1

    app.include_router(router_v1, prefix=settings.api.prefix)


def configure_static(app: FastAPI) -> None:
    app.mount("/static", static_files, name="static")


def create_app() -> FastAPI:
    deps = []
    if settings.api.mode == ApiModes.production.value:  # pragma: no cover
        deps = [
            # 114.15 req/hr over 1 year
            RateLimiter(times=1000000, hours=8760),
            # 595.23 req/hr over 1 week
            RateLimiter(times=100000, hours=168),
            # 833.33 req/hr over 1 day
            RateLimiter(times=20000, hours=24),
            # 1,000 req/hr
            RateLimiter(times=1000, hours=1),
            # 120 req/min = 7,200 req/hr
            RateLimiter(times=120, minutes=1),
            # 10 req/sec = 36,000 req/hr
            RateLimiter(times=10, seconds=1),
        ]
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
    configure_rate_limiter_exceptions(app)
    configure_static(app)
    configure_routers(app)
    return app


app: FastAPI = create_app()
