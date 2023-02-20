from typing import Any
from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from urllib import request
from usp.tree import AbstractSitemap
from usp.objects.page import SitemapPage
from uuid import UUID

from app.api.errors import ErrorCode
from app.api.exceptions import (
    ClientNotExists,
    EntityIdNotProvided,
    InvalidID,
    WebsiteMapNotExists,
    WebsiteNotExists,
    WebsitePageNotExists,
)
from app.core.logger import logger
from app.core.utilities.uuids import parse_id
from app.db.repositories import (
    ClientRepository, WebsiteRepository, WebsiteMapRepository, WebsitePageRepository
)
from app.db.session import async_session
from app.db.schemas import (
    WebsiteMapCreate,
    WebsitePageCreate,
    WebsitePageUpdate
)
from app.db.tables import Client, Website, WebsiteMap, WebsitePage


async def get_client_or_404(
    db: AsyncSession,
    client_id: Any | None = None,
) -> Client | None:  # pragma: no cover
    """Parses uuid/int and fetches client by id."""
    try:
        if client_id is None:
            raise EntityIdNotProvided()
        parsed_id: UUID = parse_id(client_id)
        client_repo: ClientRepository = ClientRepository(session=db)
        client: Client | None = await client_repo.read(entry_id=parsed_id)
        if not client:
            raise ClientNotExists()
        return client
    except (ClientNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.CLIENT_NOT_FOUND,
        )
    except EntityIdNotProvided:
        return None


async def get_website_or_404(
    db: AsyncSession,
    website_id: Any | None = None,
) -> Website | None:  # pragma: no cover
    """Parses uuid/int and fetches website by id."""
    try:
        if website_id is None:
            raise EntityIdNotProvided()
        parsed_id: UUID = parse_id(website_id)
        website_repo: WebsiteRepository = WebsiteRepository(session=db)
        website: Website | None = await website_repo.read(entry_id=parsed_id)
        if not website:
            raise WebsiteNotExists()
        return website
    except (WebsiteNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_NOT_FOUND,
        )
    except EntityIdNotProvided:
        return None


async def get_website_sitemap_or_404(
    db: AsyncSession,
    sitemap_id: Any | None = None,
) -> WebsiteMap | None:  # pragma: no cover
    """Parses uuid/int and fetches sitemap by id."""
    try:
        if sitemap_id is None:
            raise EntityIdNotProvided()
        parsed_id: UUID = parse_id(sitemap_id)
        sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
        sitemap: WebsiteMap | None = await sitemap_repo.read(entry_id=parsed_id)
        if not sitemap:
            raise WebsiteMapNotExists()
        return sitemap
    except (WebsiteMapNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_SITEMAP_NOT_FOUND,
        )
    except EntityIdNotProvided:
        return None


async def get_website_page_or_404(
    db: AsyncSession,
    page_id: Any | None = None,
) -> WebsitePage | None:  # pragma: no cover
    """Parses uuid/int and fetches website page by id."""
    try:
        if page_id is None:
            raise EntityIdNotProvided()
        parsed_id: UUID = parse_id(page_id)
        website_page_repo: WebsitePageRepository = WebsitePageRepository(session=db)
        website_page: WebsitePage | None = await website_page_repo.read(entry_id=parsed_id)
        if not website_page:
            raise WebsitePageNotExists()
        return website_page
    except (WebsitePageNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_PAGE_NOT_FOUND,
        )
    except EntityIdNotProvided:
        return None


async def create_or_update_website_page(website_id: UUID4, sitemap_id: UUID4, page: SitemapPage) -> None:
    try:
        status_code = request.urlopen(page.url).getcode()
        session: AsyncSession
        async with async_session() as session:
            pages_repo: WebsitePageRepository = WebsitePageRepository(session)
            website_page: WebsitePage | None = await pages_repo.exists_by_two(
                field_name_a='url',
                field_value_a=page.url,
                field_name_b='website_id',
                field_value_b=website_id,
            )
            if website_page is None:
                website_page: WebsitePage = await pages_repo.create(
                    schema=WebsitePageCreate(
                        url=page.url,
                        status=status_code,
                        priority=page.priority,
                        last_modified=page.last_modified,
                        change_frequency=page.change_frequency,
                        website_id=website_id,
                        sitemap_id=sitemap_id,
                    )
                )
            else:
                website_page: WebsitePage = await pages_repo.update(
                    entry=website_page,
                    schema=WebsitePageUpdate(
                        status=status_code,
                        priority=page.priority,
                        last_modified=page.last_modified,
                        change_frequency=page.change_frequency,
                    ),
                )
    except Exception as e:  # pragma: no cover
        logger.info("Error creating or updating website pages:", e)


async def save_sitemap_pages(website_id: UUID4, sitemap: AbstractSitemap) -> None:
    try:
        session: AsyncSession
        async with async_session() as session:
            sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session)
            website_map: WebsiteMap | None = await sitemap_repo.exists_by_two(
                field_name_a='url',
                field_value_a=sitemap.url,
                field_name_b='website_id',
                field_value_b=website_id,
            )
            if website_map is None:
                website_map: WebsiteMap = await sitemap_repo.create(
                    WebsiteMapCreate(url=sitemap.url, website_id=website_id)
                )
            page: SitemapPage
            for page in sitemap.all_pages():  # pragma: no cover
                await create_or_update_website_page(website_id, website_map.id, page)
    except Exception as e:
        logger.info("Error saving sitemap pages:", e)
