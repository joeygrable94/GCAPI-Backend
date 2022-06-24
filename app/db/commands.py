import databases  # type: ignore

from app.core.config import settings
from app.core.logger import logger
from app.core.user_manager.crud import crud_user_create
from app.db.session import async_engine


async def check_db_connected() -> None:
    try:
        if not str(settings.DATABASE_URI).__contains__("sqlite"):
            database = databases.Database(settings.DATABASE_URI)
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
            database = databases.Database(settings.DATABASE_URI)
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
