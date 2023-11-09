from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

from app.schemas.website import WebsiteRead
from app.schemas.website_page import WebsitePageRead

pytestmark = pytest.mark.asyncio


async def test_website_page_kwc_create_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website: WebsiteRead = await create_random_website(db_session=db_session)
    page: WebsitePageRead = await create_random_website_page(
        db_session=db_session, website_id=website.id
    )
    data_in: Dict[str, Any] = {
        "corpus": random_lower_string(5000),
        "rawtext": random_lower_string(10000),
        "website_id": str(website.id),
        "page_id": str(page.id),
    }
    response: Response = await client.post(
        "kwc/",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["corpus"] == data_in["corpus"]
    assert data["rawtext"] == data_in["rawtext"]
    assert data["website_id"] == str(website.id)
    assert data["page_id"] == str(page.id)
