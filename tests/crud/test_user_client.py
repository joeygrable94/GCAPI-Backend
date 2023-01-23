import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import UsersClientsRepository
from app.db.schemas import UserClientRead
from app.db.tables import UserClient

pytestmark = pytest.mark.asyncio


async def test_users_clients_repo_schema_read(db_session: AsyncSession) -> None:
    repo: UsersClientsRepository = UsersClientsRepository(session=db_session)
    assert repo._schema_read is UserClientRead


async def test_users_clients_repo_table(db_session: AsyncSession) -> None:
    repo: UsersClientsRepository = UsersClientsRepository(session=db_session)
    assert repo._table is UserClient
