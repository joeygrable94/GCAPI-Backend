from app.core.logger import logger
from app.entities.ipaddress.crud_utilities import (
    assign_ip_address_to_user,
    create_or_update_ipaddress,
    get_ipaddress_from_db,
)
from app.entities.ipaddress.model import Ipaddress
from app.entities.ipaddress.schemas import IpinfoResponse
from app.entities.ipaddress.utilities import get_ipinfo_details
from app.entities.website_pagespeedinsight.crud_utilities import (
    create_website_pagespeedinsights,
)
from app.entities.website_pagespeedinsight.schemas import (
    PageSpeedInsightsDevice,
    PSIDevice,
    WebsitePageSpeedInsightsBase,
)
from app.entities.website_pagespeedinsight.utilities import fetch_pagespeedinsights
from app.utilities import parse_id


async def bg_task_request_to_delete_user(user_id: str) -> None:
    # TODO: Send email to user to confirm deletion
    # TODO: flag user as pending delete.
    logger.info(
        f"User({user_id}) requested to delete their account."
    )  # pragma: no cover


async def bg_task_request_to_delete_organization(user_id: str, organization_id: str) -> None:
    # TODO: Send email to organization admin emails to confirm deletion
    # TODO: flag organization as pending delete.
    logger.info(
        f"User({user_id}) requested to delete the Organization({organization_id})."
    )  # pragma: no cover


async def bg_task_track_user_ipinfo(ip_address: str, user_id: str) -> None:
    """A background task to track the IP Address of a user.

    This function will:

        1. check if the ip_address is valid
        2. check if the ip_address is already in the database
        3. if it is not, then fetch the details from ipinfo.io
    """
    try:
        user_uuid = parse_id(user_id)
        ip_in_db: Ipaddress | None = await get_ipaddress_from_db(ip_address)
        if ip_in_db is None:
            ip_details: IpinfoResponse = get_ipinfo_details(ip_address)
            ip_in_db = await create_or_update_ipaddress(ip_address, ip_details)

        if ip_in_db is not None:
            await assign_ip_address_to_user(ipaddress=ip_in_db, user_id=user_uuid)
    except Exception as e:  # pragma: no cover
        logger.warning(f"Error fetching IP Details: {ip_address}")
        logger.warning(e)


async def bg_task_website_page_pagespeedinsights_fetch(
    website_id: str,
    page_id: str,
    fetch_url: str,
    device: PSIDevice,
) -> None:
    logger.info(
        f"Fetching PageSpeedInsights for website {website_id}, page {page_id}, URL[{fetch_url}]"
    )
    is_created: bool = False
    insights: WebsitePageSpeedInsightsBase | None = fetch_pagespeedinsights(
        fetch_url=fetch_url,
        device=PageSpeedInsightsDevice(device=device),
    )
    if insights is not None:
        await create_website_pagespeedinsights(
            website_id=website_id,
            page_id=page_id,
            insights=insights,
        )
        is_created = True
    if is_created:
        logger.info(
            f"Successfully fetched PageSpeedInsights for website {website_id}, page {page_id}, URL[{fetch_url}]"
        )
    else:  # pragma: no cover
        logger.warning(
            f"Failed to fetch PageSpeedInsights for website {website_id}, page {page_id}, URL[{fetch_url}]"
        )
    return None
