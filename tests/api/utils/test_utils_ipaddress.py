import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.ipaddress import create_random_ipaddress
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_ipaddress

from app.api.utilities import assign_ip_address_to_user
from app.core.config import settings
from app.crud import UserIpaddressRepository
from app.models import UserIpaddress

pytestmark = pytest.mark.asyncio


async def test_assign_ip_address_to_user(
    db_session: AsyncSession,
) -> None:
    ip_address = await create_random_ipaddress(db_session)
    admin_user = await get_user_by_email(db_session, settings.auth.first_admin)
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
    same_ip = random_ipaddress()
    ip_address = await create_random_ipaddress(db_session, same_ip)
    admin_user = await get_user_by_email(db_session, settings.auth.first_admin)
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