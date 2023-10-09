from typing import List
from uuid import UUID

import pytest
from fastapi.exceptions import HTTPException

from app.api.deps import (
    ClientQueryParams,
    CommonClientQueryParams,
    CommonClientWebsiteQueryParams,
    CommonWebsiteMapQueryParams,
    CommonWebsitePageQueryParams,
    CommonWebsitePageSpeedInsightsQueryParams,
    CommonWebsiteQueryParams,
    DeviceStrategyQueryParams,
    PageQueryParams,
    WebsiteMapQueryParams,
    WebsitePageQueryParams,
    WebsiteQueryParams,
    get_async_db,
    verify_content_length,
    verify_content_type,
)
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str


@pytest.mark.asyncio
async def test_dep_verify_content_length_okay() -> None:
    underload_limit: int = settings.PAYLOAD_LIMIT - 10
    await verify_content_length(content_length=underload_limit)
    assert True


@pytest.mark.asyncio
async def test_dep_verify_content_length_too_large() -> None:
    with pytest.raises(HTTPException):
        overload_limit: int = settings.PAYLOAD_LIMIT + 10
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


def test_query_page_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        PageQueryParams(page=0)
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Page number must be greater than 0"


def test_query_client_id_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        ClientQueryParams(client_id="invalid_id")
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid client ID"


def test_query_website_id_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        WebsiteQueryParams(website_id="invalid_id")
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid website ID"


def test_query_sitemap_id_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        WebsiteMapQueryParams(sitemap_id="invalid_id")
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid sitemap ID"


def test_query_page_id_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        WebsitePageQueryParams(page_id="invalid_id")
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid page ID"


def test_query_devices_param_validation() -> None:
    with pytest.raises(HTTPException) as exc_info:
        DeviceStrategyQueryParams(strategy=["invalid_strategy"])
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Invalid strategy"


def test_query_common_client_valid_params() -> None:
    test_uuid = get_uuid_str()
    params = CommonClientQueryParams(page=1, client_id=test_uuid)

    assert params.page == 1
    assert str(params.client_id) == test_uuid
    assert isinstance(params.client_id, UUID)


def test_query_common_website_valid_params() -> None:
    test_uuid = get_uuid_str()
    params = CommonWebsiteQueryParams(page=1, website_id=test_uuid)

    assert params.page == 1
    assert str(params.website_id) == test_uuid
    assert isinstance(params.website_id, UUID)


def test_query_common_website_client_valid_params() -> None:
    test_uuid = get_uuid_str()
    test_uuid_2 = get_uuid_str()
    params = CommonClientWebsiteQueryParams(
        page=1, client_id=test_uuid, website_id=test_uuid_2
    )

    assert params.page == 1
    assert str(params.client_id) == test_uuid
    assert str(params.website_id) == test_uuid_2
    assert isinstance(params.client_id, UUID)
    assert isinstance(params.website_id, UUID)


def test_query_common_website_page_valid_params() -> None:
    test_uuid = get_uuid_str()
    test_uuid_2 = get_uuid_str()
    params = CommonWebsitePageQueryParams(
        page=1, website_id=test_uuid_2, sitemap_id=test_uuid
    )

    assert params.page == 1
    assert str(params.sitemap_id) == test_uuid
    assert str(params.website_id) == test_uuid_2
    assert isinstance(params.sitemap_id, UUID)
    assert isinstance(params.website_id, UUID)


def test_query_common_website_map_valid_params() -> None:
    test_uuid = get_uuid_str()
    params = CommonWebsiteMapQueryParams(page=1, website_id=test_uuid)

    assert params.page == 1
    assert str(params.website_id) == test_uuid
    assert isinstance(params.website_id, UUID)


def test_query_common_website_pagespeedinsights_valid_params() -> None:
    test_uuid = get_uuid_str()
    test_uuid_2 = get_uuid_str()
    params = CommonWebsitePageSpeedInsightsQueryParams(
        page=1,
        website_id=test_uuid,
        page_id=test_uuid_2,
        strategy=["mobile", "desktop"],
    )

    assert params.page == 1
    assert isinstance(params.website_id, UUID)
    assert isinstance(params.page_id, UUID)
    assert isinstance(params.devices, List)
    assert str(params.website_id) == test_uuid
    assert str(params.page_id) == test_uuid_2
    assert len(params.devices) == 2
    assert "mobile" in params.devices
    assert "desktop" in params.devices
