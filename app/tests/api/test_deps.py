import pytest
from fastapi.exceptions import HTTPException

from app.api.deps import verify_content_length, verify_content_type
from app.core.config import settings


async def test_dep_verify_content_length_okay() -> None:
    overload_limit: int = settings.PAYLOAD_LIMIT - 10
    await verify_content_length(content_length=overload_limit)


async def test_dep_verify_content_length_too_large() -> None:
    with pytest.raises(HTTPException):
        overload_limit: int = settings.PAYLOAD_LIMIT + 10
        await verify_content_length(content_length=overload_limit)


async def test_dep_verify_content_type_accepted() -> None:
    await verify_content_type(content_type="pdf")
    await verify_content_type(content_type="csv")
    await verify_content_type(content_type="json")


async def test_dep_verify_content_type_not_accepted() -> None:
    with pytest.raises(HTTPException):
        await verify_content_type(content_type="c")
    with pytest.raises(HTTPException):
        await verify_content_type(content_type="py")
    with pytest.raises(HTTPException):
        await verify_content_type(content_type="zip")
