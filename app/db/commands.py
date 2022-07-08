import contextlib

import databases  # type: ignore

from app.api.deps import get_async_db
from app.api.exceptions import UserAlreadyExists
from app.core.config import settings
from app.core.logger import logger
from app.core.security import get_user_manager
from app.db.schemas import UserCreate, UserRead
from app.db.session import async_engine


async def check_db_connected() -> None:
    try:
        if not str(settings.DATABASE_URI).__contains__("sqlite"):
            database: databases.Database = databases.Database(settings.DATABASE_URI)
            if not database.is_connected:
                await database.connect()
                await database.execute("SELECT 1")
                logger.info("+ ASYCN F(X) --> MYSQL CONNECTED!")
        logger.info("Database is ready for connections. (^_^)")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> There was a problem connecting to DB...")
        raise e


async def check_db_disconnected() -> None:
    try:
        if not str(settings.DATABASE_URI).__contains__("sqlite"):
            database: databases.Database = databases.Database(settings.DATABASE_URI)
            if database.is_connected:
                await database.disconnect()
                logger.info("+ ASYNC F(X) --> MYSQL DISCONNECTED!")
        logger.info("+ ASYNC F(X) --> Database Disconnected. (-_-) Zzz")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> Failed to Disconnect Database! (@_@)")
        raise e


async def create_db_and_tables() -> None:
    from app.db.base import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("+ ASYCN F(X) --> Database tables created.")


async def drop_db_and_tables() -> None:
    from app.db.base import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("+ ASYCN F(X) --> Database tables dropped.")


get_async_db_context = contextlib.asynccontextmanager(get_async_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def crud_user_create(
    email: str, password: str, is_superuser: bool = False
) -> None:
    try:
        async with get_async_db_context() as session:
            async with get_user_manager_context(session) as user_manager:
                user: UserRead = await user_manager.create(
                    UserCreate(
                        email=email, password=password, is_superuser=is_superuser
                    )
                )
                logger.info(f"User created {user}")
    except UserAlreadyExists:
        logger.info(f"User {email} already exists")


async def create_initial_data() -> None:
    # super user
    await crud_user_create(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    # test user
    await crud_user_create(
        email=settings.TEST_NORMAL_USER,
        password=settings.TEST_NORMAL_USER_PASSWORD,
        is_superuser=False,
    )
