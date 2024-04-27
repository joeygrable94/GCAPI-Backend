from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.api.deps.get_db import AsyncDatabaseSession
from app.api.exceptions import (
    ClientNotExists,
    Ga4PropertyNotExists,
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
    ClientRepository,
    GoAnalytics4PropertyRepository,
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
    Client,
    GoAnalytics4Property,
    Note,
    Sharpspring,
    User,
    Website,
    WebsiteKeywordCorpus,
    WebsiteMap,
    WebsitePage,
    WebsitePageSpeedInsights,
)


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
