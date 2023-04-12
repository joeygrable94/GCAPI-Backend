from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from app.core.config import settings

# Session
engine: Engine = create_engine(
    url=str(settings.DATABASE_URI),
    pool_pre_ping=True,
    poolclass=SingletonThreadPool,
    echo=settings.DB_ECHO_LOG,
)

session: Any = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async Session
async_engine: AsyncEngine = create_async_engine(
    url=settings.ASYNC_DATABASE_URI, echo=settings.DB_ECHO_LOG
)

async_session: Any = async_sessionmaker(async_engine, expire_on_commit=False)


def async_session_generator() -> async_sessionmaker:
    return async_session


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async_session = async_session_generator()
    session: AsyncSession
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:  # pragma: no cover
            await session.rollback()
            raise
        finally:
            await session.close()
