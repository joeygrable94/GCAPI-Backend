from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends, HTTPException, status

from app.api.deps.get_db import AsyncDatabaseSession
from app.api.errors import ErrorCode
from app.api.exceptions import (
    ClientNotExists,
    EntityIdNotProvided,
    InvalidID,
    WebsiteMapNotExists,
    WebsiteNotExists,
    WebsitePageNotExists,
    WebsitePageSpeedInsightsNotExists,
)
from app.core.utilities.uuids import parse_id
from app.crud import (
    ClientRepository,
    WebsiteMapRepository,
    WebsitePageRepository,
    WebsitePageSpeedInsightsRepository,
    WebsiteRepository,
)
from app.models import (
    Client,
    Website,
    WebsiteMap,
    WebsitePage,
    WebsitePageSpeedInsights,
)

'''
async def get_user_or_404(
    db: AsyncDatabaseSession,
    user_id: Any | None = None,
) -> User | None:
    """Parses uuid/int and fetches user by id."""
    try:
        if user_id is None:
            raise EntityIdNotProvided()
        parsed_id: UUID = parse_id(user_id)
        user_repo: UserRepository = UserRepository(session=db)
        user: User | None = await user_repo.read(entry_id=parsed_id)
        if user is None:
            raise UserNotExists()
        return user
    except (UserNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.USER_NOT_FOUND,
        )
    except EntityIdNotProvided:
        return None


FetchUserOr404 = Annotated[User, Depends(get_user_or_404)]
'''


async def get_client_or_404(
    db: AsyncDatabaseSession,
    client_id: Any | None = None,
) -> Client | None:
    """Parses uuid/int and fetches client by id."""
    try:
        if client_id is None:
            raise EntityIdNotProvided()
        parsed_id: UUID = parse_id(client_id)
        client_repo: ClientRepository = ClientRepository(session=db)
        client: Client | None = await client_repo.read(entry_id=parsed_id)
        if client is None:
            raise ClientNotExists()
        return client
    except (ClientNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.CLIENT_NOT_FOUND,
        )
    except EntityIdNotProvided:
        return None


FetchClientOr404 = Annotated[Client, Depends(get_client_or_404)]


async def get_website_or_404(
    db: AsyncDatabaseSession,
    website_id: Any,
) -> Website | None:
    """Parses uuid/int and fetches website by id."""
    try:
        parsed_id: UUID = parse_id(website_id)
        website_repo: WebsiteRepository = WebsiteRepository(session=db)
        website: Website | None = await website_repo.read(entry_id=parsed_id)
        if website is None:
            raise WebsiteNotExists()
        return website
    except (WebsiteNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_NOT_FOUND,
        )


FetchWebsiteOr404 = Annotated[Website, Depends(get_website_or_404)]


async def get_website_map_or_404(
    db: AsyncDatabaseSession,
    sitemap_id: Any,
) -> WebsiteMap:
    """Parses uuid/int and fetches website map by id."""
    try:
        parsed_id: UUID = parse_id(sitemap_id)
        sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
        sitemap: WebsiteMap | None = await sitemap_repo.read(entry_id=parsed_id)
        if sitemap is None:
            raise WebsiteMapNotExists()
        return sitemap
    except (WebsiteMapNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_MAP_NOT_FOUND,
        )


FetchSitemapOr404 = Annotated[WebsiteMap, Depends(get_website_map_or_404)]


async def get_website_page_or_404(
    db: AsyncDatabaseSession,
    page_id: Any,
) -> WebsitePage | None:
    """Parses uuid/int and fetches website page by id."""
    try:
        parsed_id: UUID = parse_id(page_id)
        website_page_repo: WebsitePageRepository = WebsitePageRepository(session=db)
        website_page: WebsitePage | None = await website_page_repo.read(
            entry_id=parsed_id
        )
        if website_page is None:
            raise WebsitePageNotExists()
        return website_page
    except (WebsitePageNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_PAGE_NOT_FOUND,
        )


FetchWebPageOr404 = Annotated[WebsitePage, Depends(get_website_page_or_404)]


async def get_website_page_psi_or_404(
    db: AsyncDatabaseSession,
    psi_id: Any,
) -> WebsitePageSpeedInsights | None:
    """Parses uuid/int and fetches website page speed insights by id."""
    try:
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
    except (WebsitePageSpeedInsightsNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND,
        )


FetchWebPageSpeedInsightOr404 = Annotated[
    WebsitePageSpeedInsights, Depends(get_website_page_psi_or_404)
]
