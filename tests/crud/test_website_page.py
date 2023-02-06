import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import WebsitePageRepository
from app.db.tables import WebsitePage

pytestmark = pytest.mark.asyncio


async def test_website_page_repo_table(db_session: AsyncSession) -> None:
    repo: WebsitePageRepository = WebsitePageRepository(session=db_session)
    assert repo._table is WebsitePage
