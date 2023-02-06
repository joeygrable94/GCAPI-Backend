import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_ipaddress import UserIpAddressRepository
from app.db.tables.user_ipaddress import UserIpAddress

pytestmark = pytest.mark.asyncio


async def test_users_ipaddresses_repo_table(db_session: AsyncSession) -> None:
    repo: UserIpAddressRepository = UserIpAddressRepository(session=db_session)
    assert repo._table is UserIpAddress
