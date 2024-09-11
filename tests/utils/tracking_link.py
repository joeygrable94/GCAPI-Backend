from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_domain, random_lower_string

from app.crud import ClientTrackingLinkRepository, TrackingLinkRepository
from app.db.utilities import hash_url
from app.models import Client, ClientTrackingLink, TrackingLink
from app.schemas import (
    ClientRead,
    ClientTrackingLinkCreate,
    TrackingLinkCreate,
    TrackingLinkRead,
)


def build_utm_link(
    domain: str,
    url_path: str,
    utm_campaign: str | None = None,
    utm_medium: str | None = None,
    utm_source: str | None = None,
    utm_content: str | None = None,
    utm_term: str | None = None,
) -> str:
    utm_link = f"https://{domain}{url_path}?"
    if utm_campaign:
        utm_link += f"utm_campaign={utm_campaign}"
    if utm_medium:
        utm_link += f"&utm_medium={utm_medium}"
    if utm_source:
        utm_link += f"&utm_source={utm_source}"
    if utm_content:
        utm_link += f"&utm_content={utm_content}"
    if utm_term:
        utm_link += f"&utm_term={utm_term}"
    return utm_link


async def create_random_tracking_link(
    db_session: AsyncSession, is_active: bool | None = None
) -> TrackingLinkRead:
    repo: TrackingLinkRepository = TrackingLinkRepository(session=db_session)
    domain_name = random_domain()
    url_path = "/%s" % random_lower_string(16)
    utm_cmpn = random_lower_string(16)
    utm_mdm = random_lower_string(16)
    utm_src = random_lower_string(16)
    utm_cnt = random_lower_string(16)
    utm_trm = random_lower_string(16)
    tracked_url = build_utm_link(
        domain_name, url_path, utm_cmpn, utm_mdm, utm_src, utm_cnt, utm_trm
    )
    hashed_url = hash_url(tracked_url)
    tracking_link: TrackingLink = await repo.create(
        schema=TrackingLinkCreate(
            url=tracked_url,
            url_path=url_path,
            url_hash=hashed_url,
            utm_campaign=utm_cmpn,
            utm_medium=utm_mdm,
            utm_source=utm_src,
            utm_content=utm_cnt,
            utm_term=utm_trm,
            is_active=is_active if is_active is not None else True,
        )
    )
    return TrackingLinkRead.model_validate(tracking_link)


async def assign_tracking_link_to_client(
    db_session: AsyncSession,
    tracking_link: TrackingLink | TrackingLinkRead,
    client: Client | ClientRead,
) -> ClientTrackingLink:
    repo: ClientTrackingLinkRepository = ClientTrackingLinkRepository(
        session=db_session
    )
    client_tracking_link: ClientTrackingLink = await repo.create(
        schema=ClientTrackingLinkCreate(
            tracking_link_id=tracking_link.id, client_id=client.id
        )
    )
    return client_tracking_link
