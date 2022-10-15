from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
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

async_session: Any = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
