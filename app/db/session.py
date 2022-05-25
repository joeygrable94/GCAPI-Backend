from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Session
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DB_ECHO_LOG
)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Async Session
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URI,
    echo=settings.DB_ECHO_LOG
)

async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
