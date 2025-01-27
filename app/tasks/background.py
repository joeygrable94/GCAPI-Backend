from pydantic import IPvAnyAddress

from app.api.exceptions.exceptions import InvalidID
from app.api.utilities import (
    assign_ip_address_to_user,
    create_or_read_data_bucket,
    create_or_update_ipaddress,
    create_or_update_website_map,
    create_or_update_website_page,
    create_website_pagespeedinsights,
    fetch_pagespeedinsights,
    get_ipaddress_from_db,
    get_ipinfo_details,
)
from app.core.config import settings
from app.core.logger import logger
from app.core.utilities import (
    check_is_sitemap_index,
    check_is_sitemap_page,
    check_is_sitemap_urlset,
    fetch_url_page_text,
    parse_id,
    parse_sitemap_xml,
    process_sitemap_index,
    process_sitemap_page_urlset,
)
from app.models import Ipaddress
from app.schemas import (
    IpinfoResponse,
    PageSpeedInsightsDevice,
    PSIDevice,
    WebsitePageSpeedInsightsBase,
)


async def bg_task_request_to_delete_user(user_id: str) -> None:
    # TODO: Send email to user to confirm deletion
    # TODO: flag user as pending delete.
    logger.info(
        f"User({user_id}) requested to delete their account."
    )  # pragma: no cover


async def bg_task_request_to_delete_client(user_id: str, client_id: str) -> None:
    # TODO: Send email to client admin emails to confirm deletion
    # TODO: flag client as pending delete.
    logger.info(
        f"User({user_id}) requested to delete the Client({client_id})."
    )  # pragma: no cover


async def bg_task_create_client_data_bucket(
    bucket_prefix: str,
    client_id: str,
    bdx_feed_id: str | None = None,
    gcft_id: str | None = None,
    bucket_name: str = settings.cloud.aws_s3_default_bucket,
) -> None:
    try:
        await create_or_read_data_bucket(
            bucket_prefix=bucket_prefix,
            client_id=client_id,
            bdx_feed_id=bdx_feed_id,
            gcft_id=gcft_id,
            bucket_name=bucket_name,
        )
    except Exception as e:  # pragma: no cover
        logger.warning("Error creating client data bucket")
        logger.warning(e)


async def bg_task_track_user_ipinfo(ip_address: IPvAnyAddress, user_id: str) -> None:
    """A background task to track the IP Address of a user.

    This function will:

        1. check if the ip_address is valid
        2. check if the ip_address is already in the database
        3. if it is not, then fetch the details from ipinfo.io
    """
    try:
        user_uuid = parse_id(user_id)
        ip: IPvAnyAddress = ip_address
        ip_in_db: Ipaddress | None = await get_ipaddress_from_db(ip)  # type: ignore
        if ip_in_db is None:
            ip_details: IpinfoResponse = get_ipinfo_details(ip)  # type: ignore
            ip_in_db = await create_or_update_ipaddress(ip, ip_details)  # type: ignore

        if ip_in_db is not None:
            await assign_ip_address_to_user(ipaddress=ip_in_db, user_id=user_uuid)
    except Exception as e:  # pragma: no cover
        logger.warning(f"Error fetching IP Details: {ip_address}")
        logger.warning(e)


async def bg_task_website_sitemap_process_xml(
    website_id: str,
    sitemap_id: str,
    sitemap_url: str,
) -> None:
    try:
        parse_id(website_id)
        parse_id(sitemap_id)
    except InvalidID:
        return None
    sitemap_text: str = fetch_url_page_text(sitemap_url)
    sitemap_root = parse_sitemap_xml(sitemap_text)
    # Check if the sitemap is a sitemap index
    if check_is_sitemap_index(sitemap_root):
        logger.info(
            f"Processing sitemap index for website_id {website_id} from {sitemap_id} at {sitemap_url}"  # noqa: E501
        )
        sitemap_urls = process_sitemap_index(sitemap_root)
        for sm_url in sitemap_urls:
            await create_or_update_website_map(website_id, sm_url)
        logger.info(f"Discovered {len(sitemap_urls)} sitemap pages")
    # Check if the sitemap is a sitemap page
    elif check_is_sitemap_page(sitemap_root) or check_is_sitemap_urlset(sitemap_root):
        logger.info(
            f"Processing sitemap urlset for website_id {website_id} from {sitemap_id} at {sitemap_url}"  # noqa: E501
        )
        sitemap_webpages = process_sitemap_page_urlset(sitemap_root)
        for sm_page in sitemap_webpages:
            await create_or_update_website_page(website_id, sitemap_id, page=sm_page)
        logger.info(f"Processed {len(sitemap_webpages)} sitemap website page urls")
    return None


async def bg_task_website_page_pagespeedinsights_fetch(
    website_id: str,
    page_id: str,
    fetch_url: str,
    device: PSIDevice,
) -> None:
    logger.info(
        f"Fetching PageSpeedInsights for website {website_id}, page {page_id}, URL[{fetch_url}]"  # noqa: E501
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
            f"Successfully fetched PageSpeedInsights for website {website_id}, page {page_id}, URL[{fetch_url}]"  # noqa: E501
        )
    else:
        logger.warning(
            f"Failed to fetch PageSpeedInsights for website {website_id}, page {page_id}, URL[{fetch_url}]"  # noqa: E501
        )
    return None
