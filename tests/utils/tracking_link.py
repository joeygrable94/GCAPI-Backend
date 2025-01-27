from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import TrackingLinkRepository
from app.db.utilities import hash_url
from app.models import TrackingLink
from app.schemas import TrackingLinkCreate, TrackingLinkRead
from tests.utils.utils import random_domain, random_lower_string


def build_utm_link(
    scheme: str,
    domain: str,
    url_path: str,
    utm_campaign: str | None = None,
    utm_medium: str | None = None,
    utm_source: str | None = None,
    utm_content: str | None = None,
    utm_term: str | None = None,
) -> str:
    url_path = url_path if url_path.startswith("/") else f"/{url_path}"
    utm_base = f"{scheme}://{domain}{url_path}"
    utm_parts = []
    if utm_campaign:
        utm_parts.append(f"utm_campaign={utm_campaign}")
    if utm_medium:
        utm_parts.append(f"utm_medium={utm_medium}")
    if utm_source:
        utm_parts.append(f"utm_source={utm_source}")
    if utm_content:
        utm_parts.append(f"utm_content={utm_content}")
    if utm_term:
        utm_parts.append(f"utm_term={utm_term}")
    utm_end = "?" if len(utm_parts) > 0 else ""
    if len(utm_parts) > 0:
        utm_end += "&".join(utm_parts)
    utm_link = f"{utm_base}{utm_end}"
    return utm_link


async def create_random_tracking_link(
    db_session: AsyncSession,
    client_id: UUID4,
    is_active: bool | None = None,
    scheme: str | None = None,
    domain: str | None = None,
    path: str | None = None,
    utm_campaign: str | None = None,
    utm_medium: str | None = None,
    utm_source: str | None = None,
    utm_content: str | None = None,
    utm_term: str | None = None,
) -> TrackingLinkRead:
    repo: TrackingLinkRepository = TrackingLinkRepository(session=db_session)
    scheme = scheme if scheme is not None else "https"
    domain_name = domain if domain is not None else random_domain()
    url_path = path if path is not None else "/%s" % random_lower_string(16)
    utm_cmpn = random_lower_string(16) if utm_campaign is None else utm_campaign
    utm_mdm = random_lower_string(16) if utm_medium is None else utm_medium
    utm_src = random_lower_string(16) if utm_source is None else utm_source
    utm_cnt = random_lower_string(16) if utm_content is None else utm_content
    utm_trm = random_lower_string(16) if utm_term is None else utm_term
    link_active = is_active if is_active is not None else True
    destination = f"{scheme}://{domain_name}{url_path}"
    tracked_url = build_utm_link(
        scheme, domain_name, url_path, utm_cmpn, utm_mdm, utm_src, utm_cnt, utm_trm
    )
    hashed_url = hash_url(tracked_url)
    tracking_link: TrackingLink = await repo.create(
        schema=TrackingLinkCreate(
            url=tracked_url,
            url_hash=hashed_url,
            scheme=scheme,
            domain=domain_name,
            destination=destination,
            url_path=url_path,
            utm_campaign=utm_cmpn,
            utm_medium=utm_mdm,
            utm_source=utm_src,
            utm_content=utm_cnt,
            utm_term=utm_trm,
            is_active=link_active,
            client_id=client_id,
        )
    )
    return TrackingLinkRead.model_validate(tracking_link)
