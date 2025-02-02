from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import get_db_session


async def verify_content_length(content_length: int = Header(...)) -> None:
    if content_length > settings.api.payload_limit:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Files must be smaller than {settings.api.payload_limit_kb} KB.",
        )
    return None


async def verify_content_type(content_type: str = Header(...)) -> None:
    if content_type not in settings.api.allowed_mime_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid file type.",
        )
    return None


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_db_session() as session:
        yield session


AsyncDatabaseSession = Annotated[AsyncSession, Depends(get_async_db)]
