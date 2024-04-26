from pydantic.networks import IPvAnyAddress

from app.api.utilities import (
    create_or_update_ipaddress,
    get_ipaddress_from_db,
    get_ipinfo_details,
)
from app.core.logger import logger
from app.models import Ipaddress
from app.schemas import IpinfoResponse
from app.worker import task_broker


@task_broker.task(task_name="usertask:task_fetch_ipinfo")
async def task_fetch_ipinfo(
    ip_address: str,
) -> Ipaddress | None:
    try:
        # check if the ip_address is valid
        ip = IPvAnyAddress(ip_address)
        # check if the ip_address is already in the database
        ip_in_db: Ipaddress | None = await get_ipaddress_from_db(ip)
        # if it is not, then fetch the details from ipinfo.io
        if ip_in_db is None:
            ip_details: IpinfoResponse = get_ipinfo_details(ip)
            ip_in_db = await create_or_update_ipaddress(ip, ip_details)
        return ip_in_db
    except Exception as e:  # pragma: no cover
        logger.warning(f"Error fetching IP Details: {ip_address}")
        logger.warning(e)
        return None
