from ipinfo.details import Details
from pydantic import UUID4
from pydantic.networks import IPvAnyAddress
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ipinfo import ipinfo_handler
from app.core.logger import logger
from app.crud import IpaddressRepository, UserIpaddressRepository
from app.db.session import get_db_session
from app.models import Ipaddress, UserIpaddress
from app.schemas import (
    IpaddressCreate,
    IpaddressRead,
    IpinfoResponse,
    UserIpaddressCreate,
)


def get_ipinfo_details(ip_address: IPvAnyAddress) -> IpinfoResponse:
    ip_data: Details = ipinfo_handler.getDetails(ip_address)
    ip_datails: dict = ip_data.details
    country_flag_unicode_value: dict = ip_datails.get(
        "country_flag", dict(unicode=None)
    )
    country_currency_code_value: dict = ip_datails.get(
        "country_currency", dict(code=None)
    )
    continent_code_value: dict = ip_datails.get("continent", dict(code=None))
    continent_name_value: dict = ip_datails.get("continent", dict(name=None))
    return IpinfoResponse(
        address=ip_datails.get("ip", "127.0.0.1"),
        hostname=ip_datails.get("hostname", None),
        is_anycast=ip_datails.get("anycast", None),
        city=ip_datails.get("city", None),
        region=ip_datails.get("region", None),
        country=ip_datails.get("country", None),
        loc=ip_datails.get("loc", None),
        org=ip_datails.get("org", None),
        postal=ip_datails.get("postal", None),
        timezone=ip_datails.get("timezone", None),
        country_name=ip_datails.get("country_name", None),
        is_eu=ip_datails.get("isEU", None) or False,
        country_flag_url=ip_datails.get("country_flag_url", None),
        country_flag_unicode=country_flag_unicode_value.get("unicode", None),
        country_currency_code=country_currency_code_value.get("code", None),
        continent_code=continent_code_value.get("code", None),
        continent_name=continent_name_value.get("name", None),
        latitude=ip_datails.get("latitude", None),
        longitude=ip_datails.get("longitude", None),
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
        logger.warning("Error loading IpAddress from DB: %s" % e)
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
        logger.warning("Error creating or updating IpAddress: %s" % e)
        return None


async def assign_ip_address_to_user(
    ipaddress: Ipaddress | IpaddressRead, user_id: UUID4
) -> None:
    try:
        session: AsyncSession
        user_ip_repo: UserIpaddressRepository
        async with get_db_session() as session:
            user_ip_repo = UserIpaddressRepository(session)
            user_ip: UserIpaddress | None = await user_ip_repo.exists_by_fields(
                {
                    "user_id": user_id,
                    "ipaddress_id": ipaddress.id,
                }
            )
            if user_ip is None:
                user_ip = await user_ip_repo.create(
                    schema=UserIpaddressCreate(
                        user_id=user_id,
                        ipaddress_id=ipaddress.id,
                    )
                )
            logger.info(
                f"User({user_id}) assigned IP({ipaddress.address}) to their account."
            )
    except Exception as e:  # pragma: no cover
        logger.warning("Error assigning IP Address to User: %s" % e)
        return None
