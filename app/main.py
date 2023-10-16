from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.exceptions import configure_exceptions
from app.api.middleware import configure_middleware
from app.core.config import settings
from app.core.templates import static_files


def configure_routers(app: FastAPI) -> None:
    from app.api.v1 import router_v1

    app.include_router(router_v1, prefix=settings.api.prefix)


def configure_static(app: FastAPI) -> None:
    app.mount("/static", static_files, name="static")


def configure_events(app: FastAPI) -> None:
    from app.db.commands import check_db_connected, check_db_disconnected

    # startup actions
    @app.on_event("startup")
    async def on_startup() -> None:
        await check_db_connected()

    # shutdown actions
    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await check_db_disconnected()


def create_app() -> FastAPI:
    # INIT APP
    app: FastAPI = FastAPI(
        title=settings.api.name,
        version=settings.api.version,
        openapi_url="/api/v1/docs/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
    )
    # Cross-Origin Resource Sharing protection
    if settings.api.allowed_cors:
        app.add_middleware(  # pragma: no cover
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.api.allowed_cors],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
        )
    configure_middleware(app)
    configure_exceptions(app)
    configure_routers(app)
    configure_static(app)
    configure_events(app)
    return app


app: FastAPI = create_app()
