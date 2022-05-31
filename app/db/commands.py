import databases  # type: ignore

from app.core.config import settings
from app.core.logger import logger
from app.core.user_crud import create_user
from app.db.session import async_engine


async def check_db_connected():
    try:
        if not str(settings.DATABASE_URL).__contains__("sqlite"):
            database = databases.Database(settings.DATABASE_URL)
            if not database.is_connected:
                await database.connect()
                await database.execute("SELECT 1")
                logger.info("+ ASYCN F(X) --> MYSQL CONNECTED!")
        logger.info("Database is ready for connections. (^_^)")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> There was a problem connecting to DB...")
        raise e


async def check_db_disconnected():
    try:
        if not str(settings.DATABASE_URL).__contains__("sqlite"):
            database = databases.Database(settings.DATABASE_URL)
            if database.is_connected:
                await database.disconnect()
                logger.info("+ ASYNC F(X) --> MYSQL DISCONNECTED!")
        logger.info("+ ASYNC F(X) --> Database Disconnected. (-_-) Zzz")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> Failed to Disconnect Database! (@_@)")
        raise e


async def create_db_and_tables():
    from app.db.base import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("+ ASYCN F(X) --> Database tables created.")


async def create_initial_data():
    await create_user(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
