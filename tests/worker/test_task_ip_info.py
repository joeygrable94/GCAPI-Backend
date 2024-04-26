import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import IpaddressRepository
from app.models import Ipaddress
from app.tasks.user_tasks import task_fetch_ipinfo

pytestmark = pytest.mark.asyncio


async def test_worker_task_fetch_ipinfo(
    db_session: AsyncSession,
) -> None:
    ip_address = "8.8.8.8"
    result: Ipaddress | None = await task_fetch_ipinfo(ip_address)
    assert result is not None
    ip_repo = IpaddressRepository(db_session)
    ip_in_db = await ip_repo.read_by(field_name="address", field_value=ip_address)
    assert ip_in_db is not None
    assert result.address == ip_in_db.address
    assert result.hostname == ip_in_db.hostname
    assert result.is_anycast == ip_in_db.is_anycast
    assert result.city == ip_in_db.city
    assert result.region == ip_in_db.region
    assert result.country == ip_in_db.country
    assert result.loc == ip_in_db.loc
    assert result.org == ip_in_db.org
    assert result.postal == ip_in_db.postal
    assert result.timezone == ip_in_db.timezone
    assert result.country_name == ip_in_db.country_name
    assert result.is_eu == ip_in_db.is_eu
    assert result.country_flag_url == ip_in_db.country_flag_url
    assert result.country_flag_unicode == ip_in_db.country_flag_unicode
    assert result.country_currency_code == ip_in_db.country_currency_code
    assert result.continent_code == ip_in_db.continent_code
    assert result.continent_name == ip_in_db.continent_name
    assert result.latitude == ip_in_db.latitude
    assert result.longitude == ip_in_db.longitude
