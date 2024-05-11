from fastapi import Header, HTTPException, status

from app.core.config import settings


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
