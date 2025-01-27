from typing import Any

import pytest
from httpx import AsyncClient, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid
from app.models import Website
from app.schemas import WebsitePageRead, WebsiteRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.utils import random_lower_string
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


async def test_website_page_kwc_create_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website: Website | WebsiteRead = await create_random_website(db_session=db_session)
    page: WebsitePageRead = await create_random_website_page(
        db_session=db_session, website_id=website.id
    )
    data_in: dict[str, Any] = {
        "corpus": random_lower_string(5000),
        "rawtext": random_lower_string(10000),
        "website_id": str(website.id),
        "page_id": str(page.id),
    }
    response: Response = await client.post(
        "kwc/",
        headers=admin_user.token_headers,
        json=data_in,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["corpus"] == data_in["corpus"]
    assert data["rawtext"] == data_in["rawtext"]
    assert data["website_id"] == str(website.id)
    assert data["page_id"] == str(page.id)


async def test_website_page_kwc_create_website_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website_id: UUID4 = get_uuid()
    page: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session=db_session, website_id=website_id
    )
    data_in: dict[str, Any] = {
        "corpus": random_lower_string(5000),
        "rawtext": random_lower_string(10000),
        "website_id": str(website_id),
        "page_id": str(page.id),
    }
    response: Response = await client.post(
        "kwc/",
        headers=admin_user.token_headers,
        json=data_in,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]


async def test_website_page_kwc_create_website_page_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website: Website | WebsiteRead = await create_random_website(db_session=db_session)
    website_id: UUID4 = get_uuid()
    await create_random_website_page(db_session=db_session, website_id=website_id)
    page_id: UUID4 = get_uuid()
    data_in: dict[str, Any] = {
        "corpus": random_lower_string(5000),
        "rawtext": random_lower_string(10000),
        "website_id": str(website.id),
        "page_id": str(page_id),
    }
    response: Response = await client.post(
        "kwc/",
        headers=admin_user.token_headers,
        json=data_in,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]
