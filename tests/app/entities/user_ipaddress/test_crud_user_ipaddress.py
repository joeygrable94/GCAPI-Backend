import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_user_ipaddress.crud import UserIpaddressRepository
from app.entities.core_user_ipaddress.model import UserIpaddress

pytestmark = pytest.mark.asyncio


async def test_user_ipaddress_repo_table(db_session: AsyncSession) -> None:
    repo: UserIpaddressRepository = UserIpaddressRepository(session=db_session)
    assert repo._table is UserIpaddress
