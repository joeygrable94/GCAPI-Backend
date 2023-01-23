import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import WebsitesRepository
from app.db.schemas import WebsiteRead
from app.db.tables import Website

pytestmark = pytest.mark.asyncio


async def test_websites_repo_schema_read(db_session: AsyncSession) -> None:
    repo: WebsitesRepository = WebsitesRepository(session=db_session)
    assert repo._schema_read is WebsiteRead


async def test_websites_repo_table(db_session: AsyncSession) -> None:
    repo: WebsitesRepository = WebsitesRepository(session=db_session)
    assert repo._table is Website
