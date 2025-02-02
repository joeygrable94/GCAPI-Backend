import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.client.crud import ClientRepository
from app.entities.client.model import Client

pytestmark = pytest.mark.asyncio


async def test_clients_repo_table(db_session: AsyncSession) -> None:
    repo: ClientRepository = ClientRepository(session=db_session)
    assert repo._table is Client
