from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.db.tables import User
from app.core.user_manager.manager import SQLAlchemyUserDatabase


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        # await session.commit()


async def get_user_db(session: AsyncSession = Depends(get_async_db)) -> AsyncGenerator:
    yield SQLAlchemyUserDatabase(session, User)
