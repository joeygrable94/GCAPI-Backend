from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_db_session() as session:
        yield session


AsyncDatabaseSession = Annotated[AsyncSession, Depends(get_async_db)]
