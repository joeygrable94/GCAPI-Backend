import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import ClientsRepository
from app.db.schemas import ClientRead
from app.db.tables import Client

pytestmark = pytest.mark.asyncio


async def test_clients_repo_schema_read(db_session: AsyncSession) -> None:
    repo: ClientsRepository = ClientsRepository(session=db_session)
    assert repo._schema_read is ClientRead


async def test_clients_repo_table(db_session: AsyncSession) -> None:
    repo: ClientsRepository = ClientsRepository(session=db_session)
    assert repo._table is Client
