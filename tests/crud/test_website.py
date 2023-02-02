import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import WebsitesRepository
from app.db.tables import Website

pytestmark = pytest.mark.asyncio


async def test_websites_repo_table(db_session: AsyncSession) -> None:
    repo: WebsitesRepository = WebsitesRepository(session=db_session)
    assert repo._table is Website
