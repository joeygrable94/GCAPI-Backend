from fastapi import Header, HTTPException, status

from app.core.config import settings


async def verify_content_length(content_length: int = Header(...)) -> None:
    if content_length > settings.PAYLOAD_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Files must be smaller than {settings.PAYLOAD_LIMIT_KB} KB.",
        )
    return None


async def verify_content_type(content_type: str = Header(...)) -> None:
    if content_type not in settings.ACCEPTED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Incorrect file type.",
        )
    return None
