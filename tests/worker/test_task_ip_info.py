import unittest.mock

import pytest
from ipinfo.details import Details  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import get_user_by_email

from app.core.config import settings
from app.crud import IpaddressRepository, UserIpaddressRepository
from app.models import Ipaddress, UserIpaddress
from app.tasks import bg_task_track_user_ipinfo

pytestmark = pytest.mark.asyncio


mock_details = Details(
    details=dict(  # pragma: no cover
        address="8.8.8.8",
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
)


async def test_worker_task_fetch_ipinfo(
    db_session: AsyncSession,
) -> None:
    user_a = await get_user_by_email(db_session, settings.auth.first_admin)
    ip_address = "8.8.8.8"
    with unittest.mock.patch(
        "app.api.utilities.ipaddress.ipinfo_handler.getDetails"
    ) as mock_ipinfo_details:
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
