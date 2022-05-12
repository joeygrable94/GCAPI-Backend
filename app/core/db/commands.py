import databases  # type: ignore
from alembic import command
from alembic import config as migrationConfig
from app import config
from app.core.logger import logger
from app.core.db.session import async_engine
from app.core.crud.crud_user import create_user


async def check_db_connected():
    try:
        if not str(config.SQLALCHEMY_DATABASE_URI).__contains__('sqlite'):
            database = databases.Database(config.SQLALCHEMY_DATABASE_URI)
            if not database.is_connected:
                await database.connect()
                await database.execute("SELECT 1")
                logger.info('+ ASYCN F(X) --> MYSQL CONNECTED!')
        logger.info('Database is ready for connections. (^_^)')
    except Exception as e:
        logger.info('+ ASYNC F(X) --> Looks like there is some problem in connection, see below traceback.')
        raise e


async def check_db_disconnected():
    try:
        if not str(config.SQLALCHEMY_DATABASE_URI).__contains__("sqlite"):
            database = databases.Database(config.SQLALCHEMY_DATABASE_URI)
            if database.is_connected:
                await database.disconnect()
                logger.info('+ ASYNC F(X) --> MYSQL DISCONNECTED!')
        logger.info('+ ASYNC F(X) --> Database Disconnected. (-_-) Zzz')
    except Exception as e:
        logger.info('+ ASYNC F(X) --> Failed to Disconnect Database! (@_@)')
        raise e


async def create_db_and_tables():
    from app.core.db.base import Base
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info('+ ASYCN F(X) --> Database tables created.')


async def create_initial_data():
    await create_user(email=config.FIRST_SUPERUSER,
                      password=config.FIRST_SUPERUSER_PASSWORD,
                      is_superuser=True)


def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


async def run_async_upgrade():
    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, migrationConfig.Config("alembic.ini"))

