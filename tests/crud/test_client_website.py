import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import ClientsWebsitesRepository
from app.db.schemas import ClientWebsiteRead
from app.db.tables import ClientWebsite

pytestmark = pytest.mark.asyncio


async def test_clients_websites_repo_schema_read(db_session: AsyncSession) -> None:
    repo: ClientsWebsitesRepository = ClientsWebsitesRepository(session=db_session)
    assert repo._schema_read is ClientWebsiteRead


async def test_clients_websites_repo_table(db_session: AsyncSession) -> None:
    repo: ClientsWebsitesRepository = ClientsWebsitesRepository(session=db_session)
    assert repo._table is ClientWebsite
