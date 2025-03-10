import unittest.mock

import pytest
from ipinfo.details import Details  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_ipaddress.crud import IpaddressRepository
from app.entities.core_ipaddress.model import Ipaddress
from app.entities.core_user_ipaddress.crud import UserIpaddressRepository
from app.entities.core_user_ipaddress.model import UserIpaddress
from app.tasks.background import bg_task_track_user_ipinfo
from tests.utils.users import create_core_user
from tests.utils.utils import random_ipaddress

pytestmark = pytest.mark.anyio


mock_details_dict = dict(
    hostname="dns.google",
    anycast=True,
    city="Mountain View",
    region="California",
    country="US",
    loc="37.4056,-122.0775",
    org="AS15169 Google LLC",
    postal="94043",
    timezone="America/Los_Angeles",
    country_name="United States",
    isEU=False,
    country_flag_url="https://cdn.ipinfo.io/static/images/countries-flags/US.svg",
    country_flag_unicode="U+1F1FA U+1F1F8",
    country_currency_code="USD",
    continent_code="NA",
    continent_name="North America",
    latitude="37.4056",
    longitude="-122.0775",
)


async def test_worker_task_fetch_ipinfo(
    db_session: AsyncSession,
) -> None:
    user_a = await create_core_user(db_session, "admin")
    ip_address = "8.8.8.8"
    with unittest.mock.patch(
        "app.entities.core_ipaddress.utilities.ipinfo_handler.getDetails"
    ) as mock_ipinfo_details:
        mock_details = Details(
            details=dict(
                address=ip_address,
                **mock_details_dict,
            )
        )
        mock_ipinfo_details.return_value = mock_details
        await bg_task_track_user_ipinfo(ip_address, str(user_a.id))
        ip_repo = IpaddressRepository(db_session)
        user_ip_repo = UserIpaddressRepository(db_session)
        ip_in_db: Ipaddress | None = await ip_repo.read_by(
            field_name="address", field_value=ip_address
        )
        assert ip_in_db is not None
        assert str(ip_in_db.address) == mock_details.details.get("address")
        assert ip_in_db.city == mock_details.details.get("city")
        assert ip_in_db.hostname == mock_details.details.get("hostname")
        user_ip_in_db: UserIpaddress | None = await user_ip_repo.exists_by_fields(
            {
                "user_id": user_a.id,
                "ipaddress_id": ip_in_db.id,
            }
        )
        assert user_ip_in_db is not None


async def test_worker_task_fetch_ipinfo_random_ipaddress(
    db_session: AsyncSession,
) -> None:
    user_a = await create_core_user(db_session, "admin")
    ip_address = random_ipaddress()
    with unittest.mock.patch(
        "app.entities.core_ipaddress.utilities.ipinfo_handler.getDetails"
    ) as mock_ipinfo_details:
        mock_details = Details(
            details=dict(
                address=ip_address,
                **mock_details_dict,
            )
        )
        mock_ipinfo_details.return_value = mock_details
        await bg_task_track_user_ipinfo(ip_address, str(user_a.id))
        ip_repo = IpaddressRepository(db_session)
        user_ip_repo = UserIpaddressRepository(db_session)
        ip_in_db: Ipaddress | None = await ip_repo.read_by(
            field_name="address", field_value=ip_address
        )
        assert ip_in_db is not None
        assert str(ip_in_db.address) == mock_details.details.get("address")
        assert ip_in_db.city == mock_details.details.get("city")
        assert ip_in_db.hostname == mock_details.details.get("hostname")
        user_ip_in_db: UserIpaddress | None = await user_ip_repo.exists_by_fields(
            {
                "user_id": user_a.id,
                "ipaddress_id": ip_in_db.id,
            }
        )
        assert user_ip_in_db is not None
