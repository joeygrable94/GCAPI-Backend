from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app import config
from app.core.user_manager import auth_backend, fastapi_users
from app.core.templates import static_files
from app.core.schemas import UserCreate, UserRead, UserUpdate


def configure_routers(app):
    # import routers
    from app.api.v1.endpoints import public_routes, users_router, items_router
    # public routes
    app.include_router(public_routes, prefix=f"{config.API_PREFIX}", tags=["public"])
    # auth routes
    app.include_router(fastapi_users.get_auth_router(auth_backend), prefix=f"{config.API_PREFIX}/auth/jwt", tags=["auth"])
    app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix=f"{config.API_PREFIX}/auth", tags=["auth"])
    app.include_router(fastapi_users.get_reset_password_router(), prefix=f"{config.API_PREFIX}/auth", tags=["auth"])
    app.include_router(fastapi_users.get_verify_router(UserRead), prefix=f"{config.API_PREFIX}/auth", tags=["auth"])
    # user routes
    app.include_router(users_router, prefix=f"{config.API_PREFIX}/users", tags=["users"])
    app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix=f"{config.API_PREFIX}/users", tags=["users"])
    # core api routes
    app.include_router(items_router, prefix=f"{config.API_PREFIX}/items", tags=["items"])


def configure_static(app):
    app.mount("/static", static_files, name="static")


def configure_events(app):
    from app.core.db.commands import (
        check_db_connected,
        check_db_disconnected,
        # create_db_and_tables,
        # create_initial_data,
        # run_async_upgrade,
    )
    # startup actions
    @app.on_event("startup")
    async def on_startup():
        await check_db_connected()
        # await create_db_and_tables()
        # await create_initial_data()
        # await run_async_upgrade()
    # shutdown actions
    @app.on_event("shutdown")
    async def on_startup():
        await check_db_disconnected()


def create_app():
    app = FastAPI(title=config.PROJECT_NAME,
                  version=config.PROJECT_VERSION,
                  openapi_url=f'{config.API_PREFIX}/docs/openapi.json',
                  docs_url=f'{config.API_PREFIX}/docs',
                  redoc_url=f'{config.API_PREFIX}/redoc')
    if config.BACKEND_CORS_ORIGINS:
        app.add_middleware(CORSMiddleware,
                           allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
                           allow_credentials=True,
                           allow_methods=["*"],
                           allow_headers=["*"],
                           expose_headers=["*"])
    configure_routers(app)
    configure_static(app)
    configure_events(app)
    return app


app = create_app()
