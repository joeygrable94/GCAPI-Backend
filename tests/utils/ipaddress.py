from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.db.repositories import IpAddressRepository
from app.db.schemas.ipaddress import IpAddressCreate, IpAddressRead
from app.db.tables.ipaddress import IpAddress


async def create_random_ipaddress(db_session: AsyncSession) -> IpAddressRead:
    repo: IpAddressRepository = IpAddressRepository(session=db_session)
    user: IpAddress = await repo.create(
        schema=IpAddressCreate(address=random_lower_string(), is_blocked=False)
    )
    return IpAddressRead.from_orm(user)
