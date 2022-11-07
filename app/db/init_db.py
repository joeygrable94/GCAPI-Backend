from app.core.config import settings
from app.core.logger import logger
from app.db.base import Base
from app.db.repositories import UsersRepository
from app.db.schemas import UserCreate
from app.db.session import async_session, engine


def create_db_tables() -> None:
    logger.info("Creating Database Tables")
    Base.metadata.create_all(engine)
    logger.info("Database Tables Created")


def drop_db_tables() -> None:
    logger.info("Dropping Database Tables")
    Base.metadata.drop_all(engine)
    logger.info("Database Tables Dropped")


async def create_init_data() -> None:
    logger.info("Inserting Initial Data")
    async with async_session() as session:
        user_crud: UsersRepository = UsersRepository(session)
        await user_crud.create(
            schema=UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_active=True,
                is_verified=True,
                is_superuser=True,
            )
        )
        logger.info(f"{settings.FIRST_SUPERUSER} user created")
        await user_crud.create(
            schema=UserCreate(
                email=settings.TEST_NORMAL_USER,
                password=settings.TEST_NORMAL_USER_PASSWORD,
                is_active=True,
                is_verified=True,
                is_superuser=False,
            )
        )
        logger.info(f"{settings.TEST_NORMAL_USER} user created")
    logger.info("Data Inserted")


async def build_database() -> None:
    logger.info("Building Database")
    if settings.DEBUG_MODE:
        drop_db_tables()
        create_db_tables()
        await create_init_data()
    logger.info("Database Ready")
