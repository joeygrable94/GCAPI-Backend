import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsiteMapRepository
from app.models import WebsiteMap

pytestmark = pytest.mark.asyncio


async def test_website_map_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteMapRepository = WebsiteMapRepository(session=db_session)
    assert repo._table is WebsiteMap
