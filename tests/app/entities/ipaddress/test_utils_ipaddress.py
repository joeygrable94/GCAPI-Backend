import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_ipaddress.crud_utilities import assign_ip_address_to_user
from app.entities.core_user_ipaddress.crud import UserIpaddressRepository
from app.entities.core_user_ipaddress.model import UserIpaddress
from tests.utils.ipaddress import create_random_ipaddress
from tests.utils.users import create_core_user
from tests.utils.utils import random_ipaddress

pytestmark = pytest.mark.anyio


async def test_assign_ip_address_to_user(
    db_session: AsyncSession,
) -> None:
    admin_user = await create_core_user(db_session, "admin")
    ip_address = await create_random_ipaddress(db_session)
    await assign_ip_address_to_user(
        ipaddress=ip_address,
        user_id=admin_user.id,
    )
    user_ip_repo = UserIpaddressRepository(db_session)
    user_ip_address: UserIpaddress | None = await user_ip_repo.exists_by_fields(
        {
            "user_id": admin_user.id,
            "ipaddress_id": ip_address.id,
        }
    )
    assert user_ip_address is not None


async def test_assign_ip_address_to_user_repeat_ip(
    db_session: AsyncSession,
) -> None:
    admin_user = await create_core_user(db_session, "admin")
    same_ip = random_ipaddress()
    ip_address = await create_random_ipaddress(db_session, same_ip)
    await assign_ip_address_to_user(
        ipaddress=ip_address,
        user_id=admin_user.id,
    )
    await assign_ip_address_to_user(
        ipaddress=ip_address,
        user_id=admin_user.id,
    )
    user_ip_repo = UserIpaddressRepository(db_session)
    user_ip_address: UserIpaddress | None = await user_ip_repo.exists_by_fields(
        {
            "user_id": admin_user.id,
            "ipaddress_id": ip_address.id,
        }
    )
    assert user_ip_address is not None
