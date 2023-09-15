from app.core.logger import logger  # pragma: no cover
from app.db.base import Base  # pragma: no cover
from app.db.session import engine  # pragma: no cover


def create_db_tables() -> None:  # pragma: no cover
    logger.info("Creating Database Tables")
    Base.metadata.create_all(engine)
    logger.info("Database Tables Created")


def drop_db_tables() -> None:  # pragma: no cover
    logger.info("Dropping Database Tables")
    Base.metadata.drop_all(engine)
    logger.info("Database Tables Dropped")


async def create_init_data() -> None:  # pragma: no cover
    logger.info("Inserting Initial Data")
    logger.info("Data Inserted")


async def build_database() -> None:  # pragma: no cover
    logger.info("Building Database")
    drop_db_tables()
    create_db_tables()
    logger.info("Database Ready")
