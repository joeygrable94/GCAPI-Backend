from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.models import Website
from app.schemas import WebsiteKeywordCorpusRead, WebsitePageRead, WebsiteRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_keywordcorpus import create_random_website_keywordcorpus
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


async def test_website_page_kwc_read_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website: Website | WebsiteRead = await create_random_website(db_session=db_session)
    page: WebsitePageRead = await create_random_website_page(
        db_session=db_session, website_id=website.id
    )
    website_kwc: WebsiteKeywordCorpusRead = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    response: Response = await client.get(
        f"kwc/{website_kwc.id}", headers=admin_user.token_headers
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["corpus"] == website_kwc.corpus
    assert data["rawtext"] == website_kwc.rawtext
    assert data["website_id"] == str(website_kwc.website_id)
    assert data["page_id"] == str(website_kwc.page_id)


async def test_website_page_kwc_read_as_admin_kwc_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    kwc_id = get_uuid_str()
    response: Response = await client.get(
        f"kwc/{kwc_id}", headers=admin_user.token_headers
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in data["detail"]
