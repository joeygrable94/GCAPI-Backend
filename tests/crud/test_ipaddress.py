import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import IpaddressRepository
from app.models import Ipaddress

pytestmark = pytest.mark.asyncio


async def test_ipaddress_repo_table(db_session: AsyncSession) -> None:
    repo: IpaddressRepository = IpaddressRepository(session=db_session)
    assert repo._table is Ipaddress
