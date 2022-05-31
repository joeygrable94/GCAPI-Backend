import asyncio

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import logger
from app.core.user_crud import create_user


def init_db(db: Session) -> None:
    logger.info("init db data")
    asyncio.run(
        create_user(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
    )
