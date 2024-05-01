from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.api.deps.get_db import AsyncDatabaseSession
from app.api.exceptions import (
    BdxFeedNotExists,
    ClientNotExists,
    Ga4PropertyNotExists,
    Ga4StreamNotExists,
    GoCloudPropertyNotExists,
    GoSearchConsoleMetricNotExists,
    GoSearchConsolePropertyNotExists,
    NoteNotExists,
    SharpspringNotExists,
    UserNotExists,
    WebsiteMapNotExists,
    WebsiteNotExists,
    WebsitePageKeywordCorpusNotExists,
    WebsitePageNotExists,
    WebsitePageSpeedInsightsNotExists,
)
from app.core.utilities.uuids import parse_id
from app.crud import (
    BdxFeedRepository,
    ClientRepository,
    GoAnalytics4PropertyRepository,
    GoAnalytics4StreamRepository,
    GoCloudPropertyRepository,
    GoSearchConsoleMetricRepository,
    GoSearchConsolePropertyRepository,
    NoteRepository,
    SharpspringRepository,
    UserRepository,
    WebsiteKeywordCorpusRepository,
    WebsiteMapRepository,
    WebsitePageRepository,
    WebsitePageSpeedInsightsRepository,
    WebsiteRepository,
)
from app.models import (
    BdxFeed,
    Client,
    GoAnalytics4Property,
    GoAnalytics4Stream,
    GoCloudProperty,
    GoSearchConsoleCountry,
    GoSearchConsoleDevice,
    GoSearchConsolePage,
    GoSearchConsoleProperty,
    GoSearchConsoleQuery,
    GoSearchConsoleSearchappearance,
    Note,
    Sharpspring,
    User,
    Website,
    WebsiteKeywordCorpus,
    WebsiteMap,
    WebsitePage,
    WebsitePageSpeedInsights,
)
from app.schemas import GoSearchConsoleMetricType


async def get_user_or_404(
    db: AsyncDatabaseSession,
    user_id: Any,
) -> User | None:
    """Parses uuid/int and fetches user by id."""
    parsed_id: UUID = parse_id(user_id)
    user_repo: UserRepository = UserRepository(session=db)
    user: User | None = await user_repo.read(entry_id=parsed_id)
    if user is None:
        raise UserNotExists()
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
        raise ClientNotExists()
    return client


FetchClientOr404 = Annotated[Client, Depends(get_client_or_404)]


async def get_note_or_404(
    db: AsyncDatabaseSession,
    note_id: Any,
) -> Note | None:
    """Parses uuid/int and fetches note by id."""
    parsed_id: UUID = parse_id(note_id)
    note_repo: NoteRepository = NoteRepository(session=db)
    note: Note | None = await note_repo.read(entry_id=parsed_id)
    if note is None:
        raise NoteNotExists()
    return note


FetchNoteOr404 = Annotated[Note, Depends(get_note_or_404)]


async def get_website_or_404(
    db: AsyncDatabaseSession,
    website_id: Any,
) -> Website | None:
    """Parses uuid/int and fetches website by id."""
    parsed_id: UUID = parse_id(website_id)
    website_repo: WebsiteRepository = WebsiteRepository(session=db)
    website: Website | None = await website_repo.read(entry_id=parsed_id)
    if website is None:
        raise WebsiteNotExists()
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
        raise WebsiteMapNotExists()
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
        raise WebsitePageNotExists()
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
    website_page_speed_insights: WebsitePageSpeedInsights | None = (
        await website_page_psi_repo.read(parsed_id)
    )
    if website_page_speed_insights is None:
        raise WebsitePageSpeedInsightsNotExists()
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
    website_keyword_corpus: WebsiteKeywordCorpus | None = (
        await website_page_kwc_repo.read(parsed_id)
    )
    if website_keyword_corpus is None:
        raise WebsitePageKeywordCorpusNotExists()
    return website_keyword_corpus


FetchWebsiteKeywordCorpusOr404 = Annotated[
    WebsiteKeywordCorpus, Depends(get_website_page_kwc_or_404)
]


async def get_bdx_feed_404(
    db: AsyncDatabaseSession,
    bdx_id: Any,
) -> BdxFeed | None:
    """Parses uuid/int and fetches bdx_feed by id."""
    parsed_id: UUID = parse_id(bdx_id)
    bdx_repo: BdxFeedRepository = BdxFeedRepository(session=db)
    bdx_feed: BdxFeed | None = await bdx_repo.read(parsed_id)
    if bdx_feed is None:
        raise BdxFeedNotExists()
    return bdx_feed


async def get_sharpspring_404(
    db: AsyncDatabaseSession,
    ss_id: Any,
) -> Sharpspring | None:
    """Parses uuid/int and fetches sharpspring account by id."""
    parsed_id: UUID = parse_id(ss_id)
    ss_repo: SharpspringRepository = SharpspringRepository(session=db)
    ss_acct: Sharpspring | None = await ss_repo.read(parsed_id)
    if ss_acct is None:
        raise SharpspringNotExists()
    return ss_acct


async def get_go_cloud_404(
    db: AsyncDatabaseSession,
    go_cloud_id: Any,
) -> GoCloudProperty | None:
    """Parses uuid/int and fetches google cloud property by id."""
    parsed_id: UUID = parse_id(go_cloud_id)
    go_cloud_repo: GoCloudPropertyRepository = GoCloudPropertyRepository(session=db)
    go_cloud_acct: Sharpspring | None = await go_cloud_repo.read(parsed_id)
    if go_cloud_acct is None:
        raise GoCloudPropertyNotExists()
    return go_cloud_acct


async def get_ga4_property_404(
    db: AsyncDatabaseSession,
    ga4_id: Any,
) -> GoAnalytics4Property | None:
    """Parses uuid/int and fetches ga4 property by id."""
    parsed_id: UUID = parse_id(ga4_id)
    ga4_repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=db
    )
    ga4_property: GoAnalytics4Property | None = await ga4_repo.read(parsed_id)
    if ga4_property is None:
        raise Ga4PropertyNotExists()
    return ga4_property


async def get_ga4_stream_404(
    db: AsyncDatabaseSession,
    ga4_stream_id: Any,
) -> GoAnalytics4Stream | None:
    """Parses uuid/int and fetches ga4 stream by id."""
    parsed_id: UUID = parse_id(ga4_stream_id)
    ga4_stream_repo: GoAnalytics4StreamRepository = GoAnalytics4StreamRepository(
        session=db
    )
    ga4_stream: GoAnalytics4Stream | None = await ga4_stream_repo.read(parsed_id)
    if ga4_stream is None:
        raise Ga4StreamNotExists()
    return ga4_stream


async def get_go_search_console_property_404(
    db: AsyncDatabaseSession,
    gsc_id: Any,
) -> GoSearchConsoleProperty | None:
    """Parses uuid/int and fetches google search console property by id."""
    parsed_id: UUID = parse_id(gsc_id)
    gsc_repo: GoSearchConsolePropertyRepository = GoSearchConsolePropertyRepository(
        session=db
    )
    gsc_property: GoSearchConsoleProperty | None = await gsc_repo.read(parsed_id)
    if gsc_property is None:
        raise GoSearchConsolePropertyNotExists()
    return gsc_property


async def get_go_search_console_metric_404(
    db: AsyncDatabaseSession,
    metric_type: GoSearchConsoleMetricType,
    metric_id: Any,
) -> (
    GoSearchConsoleSearchappearance
    | GoSearchConsoleQuery
    | GoSearchConsolePage
    | GoSearchConsoleDevice
    | GoSearchConsoleCountry
):
    """
    Parses uuid/int and fetches google search console metric by metric type and id.
    """
    parsed_metric_id: UUID = parse_id(metric_id)
    gsc_metric_response: (
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry
        | None
    ) = None
    gsc_metric_repo = GoSearchConsoleMetricRepository(db, metric_type=metric_type)
    gsc_metric_response = await gsc_metric_repo.read(parsed_metric_id)
    if gsc_metric_response is None:
        raise GoSearchConsoleMetricNotExists()
    return gsc_metric_response
