import time

from fastapi import FastAPI
from requests import Request
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.templates import static_files
from app.core.user_manager import auth_backend, fastapi_users
from app.db.schemas import UserCreate, UserRead, UserUpdate


def configure_routers(app):
    # import routers
    from app.api.v1.endpoints import items_router, public_router, users_router

    # public routes
    app.include_router(public_router, prefix=f"{settings.API_PREFIX}", tags=["public"])
    # auth routes
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix=f"{settings.API_PREFIX}/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix=f"{settings.API_PREFIX}/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix=f"{settings.API_PREFIX}/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix=f"{settings.API_PREFIX}/auth",
        tags=["auth"],
    )
    # user routes
    app.include_router(
        users_router,
        prefix=f"{settings.API_PREFIX}/users",
        tags=["users"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix=f"{settings.API_PREFIX}/users",
        tags=["users"],
    )
    # core api routes
    app.include_router(
        items_router,
        prefix=f"{settings.API_PREFIX}/items",
        tags=["items"],
    )
    # app.include_router(
    #     clients_router,
    #     prefix=f"{settings.API_PREFIX}/clients",
    #     tags=["clients"]
    # )


def configure_static(app):
    app.mount("/static", static_files, name="static")


def configure_events(app):
    from app.db.commands import check_db_connected, check_db_disconnected

    # from app.db.commands import create_db_and_tables, create_initial_data
    # startup actions
    @app.on_event("startup")
    async def on_startup():
        await check_db_connected()
        # await create_db_and_tables()
        # await create_initial_data()

    # middlewares
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # shutdown actions
    @app.on_event("shutdown")
    async def on_shutdown():
        await check_db_disconnected()


def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        openapi_url=f"{settings.API_PREFIX}/docs/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
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


app = create_app()
