from fastapi import Depends, FastAPI

# from fastapi_pagination import add_pagination
from sentry_sdk import Client

from app.api.exceptions import configure_exceptions
from app.api.middleware import configure_middleware
from app.api.monitoring import configure_monitoring
from app.core.config import settings
from app.core.security import RateLimiter
from app.core.templates import static_files

sentry_client: Client | None = configure_monitoring()


def configure_routers(app: FastAPI) -> None:
    from app.api.v1 import router_v1

    app.include_router(router_v1, prefix=settings.api.prefix)


def configure_static(app: FastAPI) -> None:
    app.mount("/static", static_files, name="static")


def configure_events(app: FastAPI) -> None:
    from app.core.redis import redis_conn
    from app.core.security import FastAPILimiter
    from app.db.commands import check_db_connected, check_db_disconnected

    # startup actions
    @app.on_event("startup")
    async def on_startup() -> None:
        await check_db_connected()
        await FastAPILimiter.init(
            redis_conn,
            prefix="gcapi-limit",
        )

    # shutdown actions
    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await FastAPILimiter.close()
        await check_db_disconnected()


def create_app() -> FastAPI:
    deps = []
    if settings.api.mode == "production":
        deps = [
            RateLimiter(times=1000000, hours=8760),  # 114.15 req/hr over 1 year
            RateLimiter(times=100000, hours=168),  # 595.23 req/hr over 1 week
            RateLimiter(times=20000, hours=24),  # 833.33 req/hr over 1 day
            RateLimiter(times=1000, hours=1),  # 1,000 req/hr
            RateLimiter(times=120, minutes=1),  # 120 req/min = 7,200 req/hr
            RateLimiter(times=10, seconds=1),  # 10 req/sec = 36,000 req/hr
        ]
    app: FastAPI = FastAPI(
        title=settings.api.name,
        version=settings.api.version,
        openapi_url="/api/docs/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        dependencies=[Depends(dep) for dep in deps],
    )
    # add_pagination(app)
    configure_middleware(app)
    configure_exceptions(app)
    configure_events(app)
    configure_static(app)
    configure_routers(app)
    return app


app: FastAPI = create_app()
