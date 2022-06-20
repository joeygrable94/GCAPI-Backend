from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.db.tables import User


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        # await session.commit()


async def get_user_db(session: AsyncSession = Depends(get_async_db)) -> AsyncGenerator:
    yield SQLAlchemyUserDatabase(session, User)
