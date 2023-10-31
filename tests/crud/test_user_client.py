import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import UserClientRepository
from app.models import UserClient

pytestmark = pytest.mark.asyncio


async def test_user_client_repo_table(db_session: AsyncSession) -> None:
    repo: UserClientRepository = UserClientRepository(session=db_session)
    assert repo._table is UserClient
