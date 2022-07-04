import asyncio

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import logger
from app.db.commands import crud_user_create


def load_initial_data(db: Session) -> None:
    logger.info("init db data")
    asyncio.run(
        crud_user_create(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
    )
    asyncio.run(
        crud_user_create(
            email=settings.TEST_NORMAL_USER,
            password=settings.TEST_NORMAL_USER_PASSWORD,
            is_superuser=False,
        )
    )
