from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from app.core.config import settings
from app.core.logger import logger

# Session
engine: Engine = create_engine(
    url=settings.db.uri,
    pool_pre_ping=True,
    poolclass=SingletonThreadPool,
    echo=False,  # echo=settings.api.mode == "development",
)

session: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Async Session
async_engine: AsyncEngine = create_async_engine(
    url=settings.db.uri_async,
    echo=False,  # echo=settings.api.mode == "development",
)

async_session: Any = async_sessionmaker(async_engine, expire_on_commit=False)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    session: AsyncSession
    async with async_session() as session:
        try:
            session.begin()
            yield session
        except Exception as e:  # pragma: no cover
            logger.warning(e)
            await session.rollback()
            raise
        finally:
            await session.close()


@contextmanager
def get_sync_db_session() -> Generator[Session, None, None]:
    with session() as s:
        try:
            s.begin()
            yield s
        except Exception as e:  # pragma: no cover
            logger.warning(e)
            s.rollback()
            raise
        finally:
            s.close()
