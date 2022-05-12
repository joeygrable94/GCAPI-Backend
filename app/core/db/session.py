from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import config


engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True)
async_engine = create_async_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)

session_local = sessionmaker(autocommit=False,
                             autoflush=False,
                             bind=engine)
async_session_maker = sessionmaker(async_engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)
