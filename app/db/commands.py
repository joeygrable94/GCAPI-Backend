from typing import Any  # pragma: no cover

import databases  # pragma: no cover
from sqlalchemy.sql import text  # pragma: no cover

from app.core.config import settings  # pragma: no cover
from app.core.logger import logger  # pragma: no cover


async def check_db_connected() -> None:  # pragma: no cover
    try:
        dburl: str = str(settings.DATABASE_URI)
        stmt: Any = text("SELECT 1")
        if not dburl.__contains__("sqlite"):
            database: databases.Database = databases.Database(dburl)
            if not database.is_connected:
                await database.connect()
                await database.execute(stmt)
                logger.info("+ ASYCN F(X) --> MYSQL CONNECTED!")
        logger.info("Database is ready for connections. (^_^)")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> There was a problem connecting to DB...")
        raise e


async def check_db_disconnected() -> None:  # pragma: no cover
    try:
        dburl: str = str(settings.DATABASE_URI)
        if not dburl.__contains__("sqlite"):
            database: databases.Database = databases.Database(dburl)
            if database.is_connected:
                await database.disconnect()
                logger.info("+ ASYNC F(X) --> MYSQL DISCONNECTED!")
        logger.info("+ ASYNC F(X) --> Database Disconnected. (-_-) Zzz")
    except Exception as e:
        logger.info("+ ASYNC F(X) --> Failed to Disconnect Database! (@_@)")
        raise e
