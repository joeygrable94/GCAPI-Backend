import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_ipaddress.crud import IpaddressRepository
from app.entities.core_ipaddress.model import Ipaddress

pytestmark = pytest.mark.anyio


async def test_ipaddress_repo_table(db_session: AsyncSession) -> None:
    repo: IpaddressRepository = IpaddressRepository(session=db_session)
    assert repo._table is Ipaddress
