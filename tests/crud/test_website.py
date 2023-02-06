import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import WebsiteRepository
from app.db.tables import Website

pytestmark = pytest.mark.asyncio


async def test_website_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteRepository = WebsiteRepository(session=db_session)
    assert repo._table is Website
