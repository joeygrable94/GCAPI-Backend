import pytest
from fastapi.exceptions import HTTPException

from app.api.get_query import (
    ClientIdQueryParams,
    DeviceStrategyQueryParams,
    WebsiteIdQueryParams,
    WebsiteMapIdQueryParams,
    WebsitePageIdQueryParams,
)
from app.config import settings
from app.entities.api.dependencies import (
    get_async_db,
    verify_content_length,
    verify_content_type,
)


@pytest.mark.asyncio
async def test_dep_verify_content_length_okay() -> None:
    underload_limit: int = settings.api.payload_limit - 10
    await verify_content_length(content_length=underload_limit)
    assert True


@pytest.mark.asyncio
async def test_dep_verify_content_length_too_large() -> None:
    with pytest.raises(HTTPException):
        overload_limit: int = settings.api.payload_limit + 10
        await verify_content_length(content_length=overload_limit)


@pytest.mark.asyncio
async def test_dep_verify_content_type_accepted() -> None:
    await verify_content_type(content_type="pdf")
    await verify_content_type(content_type="csv")
    await verify_content_type(content_type="json")
    assert True


@pytest.mark.asyncio
async def test_dep_verify_content_type_not_accepted() -> None:
    with pytest.raises(HTTPException):
        await verify_content_type(content_type="c")
    with pytest.raises(HTTPException):
        await verify_content_type(content_type="py")
    with pytest.raises(HTTPException):
        await verify_content_type(content_type="zip")


@pytest.mark.asyncio
async def test_get_async_db() -> None:
    async for session in get_async_db():
        assert session is not None


def test_query_client_id_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        ClientIdQueryParams(client_id="invalid_id")
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid client ID"


def test_query_website_id_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        WebsiteIdQueryParams(website_id="invalid_id")
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid website ID"


def test_query_sitemap_id_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        WebsiteMapIdQueryParams(sitemap_id="invalid_id")
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid sitemap ID"


def test_query_page_id_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        WebsitePageIdQueryParams(page_id="invalid_id")
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid page ID"


def test_query_devices_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        DeviceStrategyQueryParams(strategy=["invalid_strategy"])
    assert exc_info.value.status_code == 422
    assert (
        exc_info.value.detail
        == "Invalid device strategy, must be 'mobile' or 'desktop'"
    )
