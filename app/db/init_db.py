from app.core.config import settings
from app.core.logger import logger
from app.db.base import Base
from app.db.session import engine


def create_db_tables() -> None:
    logger.info("Creating Database Tables")
    Base.metadata.create_all(engine)
    logger.info("Database Tables Created")


def drop_db_tables() -> None:
    logger.info("Dropping Database Tables")
    Base.metadata.drop_all(engine)
    logger.info("Database Tables Dropped")


def build_database() -> None:
    logger.info("Building Database")
    if settings.DEBUG_MODE:
        drop_db_tables()
        create_db_tables()
    logger.info("Database Ready")
