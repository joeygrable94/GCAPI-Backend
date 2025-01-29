from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.api.deps.get_db import AsyncDatabaseSession
from app.api.exceptions import ClientNotFound, EntityNotFound, UserNotFound
from app.core.utilities import parse_id
from app.crud import (
    ClientRepository,
    GoAnalytics4PropertyRepository,
    GoSearchConsolePropertyRepository,
    PlatformRepository,
    TrackingLinkRepository,
    UserRepository,
    WebsiteKeywordCorpusRepository,
    WebsiteMapRepository,
    WebsitePageRepository,
    WebsitePageSpeedInsightsRepository,
    WebsiteRepository,
)
from app.crud.go_a4_stream import GoAnalytics4StreamRepository
from app.crud.go_ads import GoAdsPropertyRepository
from app.models import (
    Client,
    GoAnalytics4Property,
    GoSearchConsoleProperty,
    Platform,
    TrackingLink,
    User,
    Website,
    WebsiteKeywordCorpus,
    WebsiteMap,
    WebsitePage,
    WebsitePageSpeedInsights,
)
from app.models.go_a4_stream import GoAnalytics4Stream
from app.models.go_ads import GoAdsProperty
from app.schemas.go import GooglePlatformType


async def get_user_or_404(
    db: AsyncDatabaseSession,
    user_id: Any,
) -> User | None:
    """Parses uuid/int and fetches user by id."""
    parsed_id: UUID = parse_id(user_id)
    user_repo: UserRepository = UserRepository(session=db)
    user: User | None = await user_repo.read(entry_id=parsed_id)
    if user is None:
        raise UserNotFound()
    return user


FetchUserOr404 = Annotated[User, Depends(get_user_or_404)]


async def get_client_or_404(
    db: AsyncDatabaseSession,
    client_id: Any,
) -> Client | None:
    """Parses uuid/int and fetches client by id."""
    parsed_id: UUID = parse_id(client_id)
    client_repo: ClientRepository = ClientRepository(session=db)
    client: Client | None = await client_repo.read(entry_id=parsed_id)
    if client is None:
        raise ClientNotFound()
    return client


FetchClientOr404 = Annotated[Client, Depends(get_client_or_404)]


async def get_platform_404(
    db: AsyncDatabaseSession,
    platform_id: Any,
) -> Platform | None:
    """Parses uuid/int and fetches platform by id."""
    parsed_id: UUID = parse_id(platform_id)
    platform_repo: PlatformRepository = PlatformRepository(session=db)
    platform: Platform | None = await platform_repo.read(parsed_id)
    if platform is None:
        raise EntityNotFound(entity_info="Platform {}".format(parsed_id))
    return platform


FetchPlatformOr404 = Annotated[Client, Depends(get_platform_404)]


async def get_tracking_link_or_404(
    db: AsyncDatabaseSession,
    tracking_link_id: Any,
) -> TrackingLink | None:
    """Parses uuid/int and fetches tracking_link by id."""
    parsed_id: UUID = parse_id(tracking_link_id)
    link_repo: TrackingLinkRepository = TrackingLinkRepository(session=db)
    link: TrackingLink | None = await link_repo.read(entry_id=parsed_id)
    if link is None:
        raise EntityNotFound(entity_info="TrackingLink {}".format(parsed_id))
    return link


FetchTrackingLinkOr404 = Annotated[TrackingLink, Depends(get_tracking_link_or_404)]


async def get_website_or_404(
    db: AsyncDatabaseSession,
    website_id: Any,
) -> Website | None:
    """Parses uuid/int and fetches website by id."""
    parsed_id: UUID = parse_id(website_id)
    website_repo: WebsiteRepository = WebsiteRepository(session=db)
    website: Website | None = await website_repo.read(entry_id=parsed_id)
    if website is None:
        raise EntityNotFound(entity_info="Website {}".format(parsed_id))
    return website


FetchWebsiteOr404 = Annotated[Website, Depends(get_website_or_404)]


async def get_website_map_or_404(
    db: AsyncDatabaseSession,
    sitemap_id: Any,
) -> WebsiteMap:
    """Parses uuid/int and fetches website map by id."""
    parsed_id: UUID = parse_id(sitemap_id)
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
    sitemap: WebsiteMap | None = await sitemap_repo.read(entry_id=parsed_id)
    if sitemap is None:
        raise EntityNotFound(entity_info="WebsiteMap {}".format(parsed_id))
    return sitemap


FetchSitemapOr404 = Annotated[WebsiteMap, Depends(get_website_map_or_404)]


async def get_website_page_or_404(
    db: AsyncDatabaseSession,
    page_id: Any,
) -> WebsitePage | None:
    """Parses uuid/int and fetches website page by id."""
    parsed_id: UUID = parse_id(page_id)
    website_page_repo: WebsitePageRepository = WebsitePageRepository(session=db)
    website_page: WebsitePage | None = await website_page_repo.read(entry_id=parsed_id)
    if website_page is None:
        raise EntityNotFound(entity_info="WebsitePage {}".format(parsed_id))
    return website_page


FetchWebPageOr404 = Annotated[WebsitePage, Depends(get_website_page_or_404)]


async def get_website_page_psi_or_404(
    db: AsyncDatabaseSession,
    psi_id: Any,
) -> WebsitePageSpeedInsights | None:
    """Parses uuid/int and fetches website page speed insights by id."""
    parsed_id: UUID = parse_id(psi_id)
    website_page_psi_repo: WebsitePageSpeedInsightsRepository = (
        WebsitePageSpeedInsightsRepository(session=db)
    )
    website_page_speed_insights: (
        WebsitePageSpeedInsights | None
    ) = await website_page_psi_repo.read(parsed_id)
    if website_page_speed_insights is None:
        raise EntityNotFound(
            entity_info="WebsitePageSpeedInsights {}".format(parsed_id)
        )
    return website_page_speed_insights


FetchWebPageSpeedInsightOr404 = Annotated[
    WebsitePageSpeedInsights, Depends(get_website_page_psi_or_404)
]


async def get_website_page_kwc_or_404(
    db: AsyncDatabaseSession,
    kwc_id: Any,
) -> WebsiteKeywordCorpus | None:
    """Parses uuid/int and fetches website keyword corpus by id."""
    parsed_id: UUID = parse_id(kwc_id)
    website_page_kwc_repo: WebsiteKeywordCorpusRepository = (
        WebsiteKeywordCorpusRepository(session=db)
    )
    website_keyword_corpus: (
        WebsiteKeywordCorpus | None
    ) = await website_page_kwc_repo.read(parsed_id)
    if website_keyword_corpus is None:
        raise EntityNotFound(
            entity_info="WebsitePageKeywordCorpus {}".format(parsed_id)
        )
    return website_keyword_corpus


FetchWebsiteKeywordCorpusOr404 = Annotated[
    WebsiteKeywordCorpus, Depends(get_website_page_kwc_or_404)
]


async def get_go_property_or_404(
    db: AsyncDatabaseSession,
    platform_type: GooglePlatformType,
    go_property_id: Any,
) -> (
    GoAnalytics4Property | GoAnalytics4Stream | GoSearchConsoleProperty | GoAdsProperty
):
    """Parses uuid/int and fetches go property by platform_type and id."""
    parsed_id: UUID = parse_id(go_property_id)
    if platform_type == GooglePlatformType.ga4:
        ga4_repo = GoAnalytics4PropertyRepository(session=db)
        ga4_property: GoAnalytics4Property | None = await ga4_repo.read(parsed_id)
        if ga4_property is None:
            raise EntityNotFound(
                entity_info="GoAnalytics4Property id = {}".format(parsed_id)
            )
        return ga4_property
    elif platform_type == GooglePlatformType.ga4_stream:
        ga4_stream_repo = GoAnalytics4StreamRepository(session=db)
        ga4_stream: GoAnalytics4Stream | None = await ga4_stream_repo.read(parsed_id)
        if ga4_stream is None:
            raise EntityNotFound(
                entity_info="GoAnalytics4Stream id = {}".format(parsed_id)
            )
        return ga4_stream
    elif platform_type == GooglePlatformType.gsc:
        gsc_repo = GoSearchConsolePropertyRepository(session=db)
        gsc_property: GoSearchConsoleProperty | None = await gsc_repo.read(parsed_id)
        if gsc_property is None:
            raise EntityNotFound(
                entity_info="GoSearchConsoleProperty id = {}".format(parsed_id)
            )
        return gsc_property
    elif platform_type == GooglePlatformType.gads:
        gads_repo = GoAdsPropertyRepository(session=db)
        gads_property: GoAdsProperty | None = await gads_repo.read(parsed_id)
        if gads_property is None:
            raise EntityNotFound(entity_info="GoAdsProperty = {}".format(parsed_id))
        return gads_property
    raise EntityNotFound(  # pragma: no cover - safety net fallback
        entity_info="GoogleProperty type = {}, id = {}".format(platform_type, parsed_id)
    )


FetchGooglePropertyOr404 = Annotated[
    GoAnalytics4Property | GoAnalytics4Stream | GoSearchConsoleProperty | GoAdsProperty,
    Depends(get_go_property_or_404),
]
