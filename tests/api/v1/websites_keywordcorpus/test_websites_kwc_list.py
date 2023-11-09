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


async def test_website_page_kwc_list_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website: WebsiteRead = await create_random_website(db_session=db_session)
    page: WebsitePageRead = await create_random_website_page(
        db_session=db_session, website_id=website.id
    )
    entry_1: WebsiteKeywordCorpusRead = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    entry_2: WebsiteKeywordCorpusRead = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    entry_3: WebsiteKeywordCorpusRead = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    response: Response = await client.get("kwc/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    all_entries: Any = response.json()
    assert len(all_entries) > 1
    for entry in all_entries:
        assert "corpus" in entry
        assert "rawtext" in entry
        assert "website_id" in entry
        assert "page_id" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["corpus"] == entry_1.corpus
            assert entry["rawtext"] == entry_1.rawtext
        if entry["id"] == str(entry_2.id):
            assert entry["corpus"] == entry_2.corpus
            assert entry["rawtext"] == entry_2.rawtext
        if entry["id"] == str(entry_3.id):
            assert entry["corpus"] == entry_3.corpus
            assert entry["rawtext"] == entry_3.rawtext
