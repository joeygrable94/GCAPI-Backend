from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_keywordcorpus import create_random_website_keywordcorpus
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

from app.schemas.website import WebsiteRead
from app.schemas.website_keywordcorpus import WebsiteKeywordCorpusRead
from app.schemas.website_page import WebsitePageRead

pytestmark = pytest.mark.asyncio


async def test_website_page_kwc_delete_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website: WebsiteRead = await create_random_website(db_session=db_session)
    page: WebsitePageRead = await create_random_website_page(
        db_session=db_session, website_id=website.id
    )
    website_kwc: WebsiteKeywordCorpusRead = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    response: Response = await client.delete(
        f"kwc/{website_kwc.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data is None
