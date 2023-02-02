import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.ipaddress import IpAddressRepository
from app.db.tables.ipaddress import IpAddress

pytestmark = pytest.mark.asyncio


async def test_ipaddresses_repo_table(db_session: AsyncSession) -> None:
    repo: IpAddressRepository = IpAddressRepository(session=db_session)
    assert repo._table is IpAddress
