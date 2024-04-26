import sys

from ipinfo.details import Details  # type: ignore
from pydantic.networks import IPvAnyAddress
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ipinfo import ipinfo_handler
from app.core.logger import logger
from app.crud import IpaddressRepository
from app.db.session import get_db_session
from app.models import Ipaddress
from app.schemas import IpinfoResponse
from app.schemas.ipaddress import IpaddressCreate

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


def get_ipinfo_details(ip_address: IPvAnyAddress) -> IpinfoResponse:
    ip_data: Details
    ip_data = (
        mock_details
        if "pytest" in sys.modules
        else ipinfo_handler.getDetails(ip_address)
    )  # pragma: no cover  # noqa: E501
    country_flag_unicode_value: dict = ip_data.details.get(
        "country_flag", dict(unicode=None)
    )
    country_currency_code_value: dict = ip_data.details.get(
        "country_currency", dict(code=None)
    )
    continent_code_value: dict = ip_data.details.get("continent", dict(code=None))
    continent_name_value: dict = ip_data.details.get("continent", dict(name=None))
    return IpinfoResponse(
        address=ip_data.details.get("ip", "127.0.0.1"),
        hostname=ip_data.details.get("hostname", None),
        is_anycast=ip_data.details.get("anycast", None),
        city=ip_data.details.get("city", None),
        region=ip_data.details.get("region", None),
        country=ip_data.details.get("country", None),
        loc=ip_data.details.get("loc", None),
        org=ip_data.details.get("org", None),
        postal=ip_data.details.get("postal", None),
        timezone=ip_data.details.get("timezone", None),
        country_name=ip_data.details.get("country_name", None),
        is_eu=ip_data.details.get("isEU", None) or False,
        country_flag_url=ip_data.details.get("country_flag_url", None),
        country_flag_unicode=country_flag_unicode_value.get("unicode", None),
        country_currency_code=country_currency_code_value.get("code", None),
        continent_code=continent_code_value.get("code", None),
        continent_name=continent_name_value.get("name", None),
        latitude=ip_data.details.get("latitude", None),
        longitude=ip_data.details.get("longitude", None),
    )


async def get_ipaddress_from_db(ip: IPvAnyAddress) -> Ipaddress | None:
    try:
        fetch_ip: Ipaddress | None = None
        session: AsyncSession
        ip_repo: IpaddressRepository
        async with get_db_session() as session:
            ip_repo = IpaddressRepository(session)
            fetch_ip = await ip_repo.read_by(
                field_name="address",
                field_value=str(ip),
            )
        return fetch_ip
    except Exception as e:  # pragma: no cover
        logger.warning("Error fetching or creating Website Page: %s" % e)
        return None


async def create_or_update_ipaddress(
    ip: IPvAnyAddress, ip_details: IpinfoResponse
) -> Ipaddress | None:
    try:
        fetch_ip: Ipaddress | None = None
        session: AsyncSession
        ip_repo: IpaddressRepository
        async with get_db_session() as session:
            ip_repo = IpaddressRepository(session)
            fetch_ip = await ip_repo.read_by(
                field_name="address",
                field_value=str(ip),
            )
            if fetch_ip is None:
                fetch_ip = await ip_repo.create(
                    schema=IpaddressCreate(
                        address=str(ip),
                        hostname=ip_details.hostname,
                        is_anycast=ip_details.is_anycast,
                        city=ip_details.city,
                        region=ip_details.region,
                        country=ip_details.country,
                        loc=ip_details.loc,
                        org=ip_details.org,
                        postal=ip_details.postal,
                        timezone=ip_details.timezone,
                        country_name=ip_details.country_name,
                        is_eu=ip_details.is_eu,
                        country_flag_url=ip_details.country_flag_url,
                        country_flag_unicode=ip_details.country_flag_unicode,
                        country_currency_code=ip_details.country_currency_code,
                        continent_code=ip_details.continent_code,
                        continent_name=ip_details.continent_name,
                        latitude=ip_details.latitude,
                        longitude=ip_details.longitude,
                    )
                )
        return fetch_ip
    except Exception as e:  # pragma: no cover
        logger.warning("Error fetching or creating Website Page: %s" % e)
        return None
