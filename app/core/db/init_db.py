from sqlalchemy.orm import Session
import asyncio

from app import config
from app.core.logger import logger
from app.core.crud.crud_user import create_user

from app.core.db.base import Base  # noqa: F401
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
	logger.info('init db data')
	asyncio.run(
		create_user(email=config.FIRST_SUPERUSER,
					password=config.FIRST_SUPERUSER_PASSWORD,
					is_superuser=True)
	)
