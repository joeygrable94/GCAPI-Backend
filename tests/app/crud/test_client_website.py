import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import ClientWebsiteRepository
from app.models import ClientWebsite

pytestmark = pytest.mark.asyncio


async def test_clients_websites_repo_table(db_session: AsyncSession) -> None:
    repo: ClientWebsiteRepository = ClientWebsiteRepository(session=db_session)
    assert repo._table is ClientWebsite
