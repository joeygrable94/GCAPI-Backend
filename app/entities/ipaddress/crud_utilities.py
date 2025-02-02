from pydantic import UUID4
from pydantic.networks import IPvAnyAddress
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.db.session import get_db_session
from app.entities.ipaddress.crud import IpaddressRepository
from app.entities.ipaddress.model import Ipaddress
from app.entities.ipaddress.schemas import (
    IpaddressCreate,
    IpaddressRead,
    IpinfoResponse,
)
from app.entities.user_ipaddress.crud import UserIpaddressRepository
from app.entities.user_ipaddress.model import UserIpaddress
from app.entities.user_ipaddress.schemas import UserIpaddressCreate


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
