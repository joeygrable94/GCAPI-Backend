import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website_page.crud import WebsitePageRepository
from app.entities.website_page.model import WebsitePage

pytestmark = pytest.mark.anyio


async def test_website_page_repo_table(db_session: AsyncSession) -> None:
    repo: WebsitePageRepository = WebsitePageRepository(session=db_session)
    assert repo._table is WebsitePage
