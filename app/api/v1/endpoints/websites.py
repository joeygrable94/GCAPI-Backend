from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.api.errors import ErrorCode
from app.api.exceptions import (
    WebsiteAlreadyExists,
    WebsiteNotExists,
    WebsiteDomainInvalid,
    WebsiteMapNotExists,
    WebsitePageNotExists,
)
from app.api.utils import (
    get_client_or_404,
    get_website_or_404,
    get_website_sitemap_or_404,
    get_website_page_or_404,
)
from app.core.config import Settings, get_settings
from app.core.logger import logger
from app.db.repositories import (
    WebsiteRepository,
    ClientWebsiteRepository,
    WebsiteMapRepository,
    WebsitePageRepository,
)
from app.db.schemas import (
    ClientRead,
    ClientWebsiteCreate,
    UserAdmin,
    WebsiteCreate,
    WebsiteRead,
    WebsiteUpdate,
    WebsiteCreateProcessing,
    WebsiteReadRelations,
    WebsiteMapRead,
    WebsiteMapReadRelations,
    WebsitePageRead,
    WebsitePageReadRelations,
)
from app.db.tables import ClientWebsite, Website, WebsiteMap, WebsitePage
from app.security import Permission, get_current_active_user
from app.worker import task_process_website_map

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="websites:read_websites",
    response_model=List[WebsiteReadRelations],
)
async def website_list(
    db: AsyncSession = Depends(get_async_db),
    page: int = 1,
    current_user: UserAdmin = Permission("list", get_current_active_user),
) -> List[WebsiteRead] | List:
    websites_repo: WebsiteRepository = WebsiteRepository(session=db)
    websites: List[Website] | List[None] | None = await websites_repo.list(page=page)
    if websites and len(websites):  # pragma: no cover
        return [WebsiteRead.from_orm(w) for w in websites]
    return []  # pragma: no cover


@router.post(
    "/",
    name="websites:create_website",
    response_model=WebsiteCreateProcessing,
)
async def website_create(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_in: WebsiteCreate,
    client_id: Any | None = None,
    current_user: UserAdmin = Permission("create", get_current_active_user),
    settings: Settings = Depends(get_settings),
) -> WebsiteCreateProcessing:
    try:  # pragma: no cover
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        data: Dict[str, str] = website_in.dict()
        check_domain: Optional[str] = data.get("domain")
        if check_domain:
            a_site: Optional[Website] = await websites_repo.read_by(
                field_name="domain",
                field_value=check_domain,
            )
            if a_site:
                raise WebsiteAlreadyExists()
        if not websites_repo.validate(domain=check_domain):
            raise WebsiteDomainInvalid()
        new_site: Website = await websites_repo.create(website_in)
        sitemap_task = task_process_website_map.delay(
            website_id=new_site.id,
            sitemap_url=new_site.get_link()
        )
        # check user has permission to assign clients to websites
        client: Optional[ClientRead] = await get_client_or_404(
            db=db, client_id=client_id
        )
        if client is not None:
            client_website_repo: ClientWebsiteRepository = ClientWebsiteRepository(
                session=db
            )
            client_site_exists: ClientWebsite | None = (
                await client_website_repo.exists_by_two(
                    field_name_a="client_id",
                    field_value_a=client.id,
                    field_name_b="website_id",
                    field_value_b=new_site.id,
                )
            )
            if client_site_exists is None:
                client_site_rel: ClientWebsite = await client_website_repo.create(
                    schema=ClientWebsiteCreate(
                        client_id=client.id, website_id=new_site.id
                    )
                )
                if settings.DEBUG_MODE:
                    logger.info(
                        f"website [{client_site_rel.website_id}] created with association to client [{client_site_rel.client_id}]"  # noqa: E501
                    )
        return WebsiteCreateProcessing(
            website=WebsiteRead.from_orm(new_site),
            sitemap_task_id=sitemap_task.id
        )
    except WebsiteDomainInvalid:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Website domain is not a valid domain"
        )
    except WebsiteAlreadyExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Website domain exists"
        )


@router.get(
    "/{website_id}",
    name="websites:read_website",
    response_model=WebsiteReadRelations,
)
async def website_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_id: Any,
    current_user: UserAdmin = Permission("read", get_current_active_user),
) -> WebsiteRead:
    website: Website | None = await get_website_or_404(db, website_id)
    return WebsiteRead.from_orm(website)  # pragma: no cover


@router.patch(
    "/{website_id}",
    name="websites:update_website",
    response_model=WebsiteReadRelations,
)
async def website_update(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_id: Any,
    website_in: WebsiteUpdate,
    current_user: UserAdmin = Permission("update", get_current_active_user),
) -> WebsiteRead:
    try:  # pragma: no cover
        website: Website | None = await get_website_or_404(db, website_id)
        if not website:
            raise WebsiteNotExists()
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        data: Dict = website_in.dict()
        check_domain: Optional[str] = data.get("domain")
        if check_domain:
            domain_found: Optional[Website] = await websites_repo.read_by(
                field_name="domain",
                field_value=check_domain,
            )
            if domain_found:
                raise WebsiteAlreadyExists()
        updated_website: Optional[Website] = await websites_repo.update(
            entry=website, schema=website_in
        )
        if not updated_website:
            raise WebsiteNotExists()
        return WebsiteRead.from_orm(updated_website)
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_NOT_FOUND
        )
    except WebsiteAlreadyExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Website domain exists"
        )


@router.delete(
    "/{website_id}",
    name="websites:delete_website",
    response_model=None,
)
async def website_delete(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_id: Any,
    current_user: UserAdmin = Permission("delete", get_current_active_user),
) -> None:
    try:  # pragma: no cover
        website: Website | None = await get_website_or_404(db, website_id)
        if not website:
            raise WebsiteNotExists()
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        await websites_repo.delete(entry=website)
        return None
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_NOT_FOUND
        )


@router.get(
    "/{website_id}/sitemaps/",
    name="websites:list_website_sitemaps",
    response_model=List[WebsiteMapReadRelations],
)
async def website_sitemaps_list(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_id: Any,
    page: int = 1,
    current_user: UserAdmin = Permission("read", get_current_active_user),
) -> List[WebsiteMapRead]:
    try:  # pragma: no cover
        website: Website | None = await get_website_or_404(db, website_id)
        if not website:
            raise WebsiteNotExists()
        sitemaps_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
        sitemaps: List[WebsiteMap] | List[None] | None = await sitemaps_repo.list(
            page=page, website_id=website.id
        )
        if sitemaps and len(sitemaps):  # pragma: no cover
            return [WebsiteMapRead.from_orm(sm) for sm in sitemaps]
        return []  # pragma: no cover
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_NOT_FOUND
        )


@router.get(
    "/{website_id}/sitemaps/{sitemap_id}",
    name="websites:read_website_sitemap",
    response_model=WebsiteMapReadRelations,
)
async def website_sitemaps_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_id: Any,
    sitemap_id: Any,
    current_user: UserAdmin = Permission("read", get_current_active_user),
) -> WebsiteMapRead:
    try:  # pragma: no cover
        website: Website | None = await get_website_or_404(db, website_id)
        if not website:
            raise WebsiteNotExists()
        sitemap: WebsiteMap | None = await get_website_sitemap_or_404(db, sitemap_id)
        if not sitemap:
            raise WebsiteMapNotExists()
        return WebsiteMapRead.from_orm(sitemap)
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_NOT_FOUND
        )
    except WebsiteMapNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_SITEMAP_NOT_FOUND
        )


@router.get(
    "/{website_id}/sitemaps/{sitemap_id}/pages/",
    name="websites:list_website_sitemap_pages",
    response_model=List[WebsitePageReadRelations],
)
async def website_sitemaps_pages_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_id: Any,
    sitemap_id: Any,
    page: int = 1,
    current_user: UserAdmin = Permission("read", get_current_active_user),
) -> List[WebsitePageRead] | List:
    try:  # pragma: no cover
        website: Website | None = await get_website_or_404(db, website_id)
        if not website:
            raise WebsiteNotExists()
        sitemap: WebsiteMap | None = await get_website_sitemap_or_404(db, sitemap_id)
        if not sitemap:
            raise WebsiteMapNotExists()
        website_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
        website_pages: List[WebsitePage] | List[None] | None = await website_pages_repo.list(
            page=page, website_id=website.id, sitemap_id=sitemap.id
        )
        if website_pages and len(website_pages):  # pragma: no cover
            return [WebsitePageRead.from_orm(pg) for pg in website_pages]
        return []  # pragma: no cover
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_NOT_FOUND
        )
    except WebsiteMapNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_SITEMAP_NOT_FOUND
        )


@router.get(
    "/{website_id}/pages/",
    name="websites:list_website_pages",
    response_model=WebsitePageReadRelations,
)
async def website_pages_list(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_id: Any,
    page: int = 1,
    current_user: UserAdmin = Permission("read", get_current_active_user),
) -> WebsitePageRead:
    try:  # pragma: no cover
        website: Website | None = await get_website_or_404(db, website_id)
        if not website:
            raise WebsiteNotExists()
        webpages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
        await webpages_repo.list(page, website_id=website.id)
        website_pages: List[WebsiteMap] | List[None] | None = await webpages_repo.list(
            page=page, website_id=website.id
        )
        if website_pages and len(website_pages):  # pragma: no cover
            return [WebsitePageRead.from_orm(pg) for pg in website_pages]
        return []  # pragma: no cover
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_NOT_FOUND
        )


@router.get(
    "/{website_id}/pages/{page_id}",
    name="websites:read_website_page",
    response_model=WebsitePageReadRelations,
)
async def website_pages_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_id: Any,
    page_id: Any,
    current_user: UserAdmin = Permission("read", get_current_active_user),
) -> WebsitePageRead:
    try:  # pragma: no cover
        website: Website | None = await get_website_or_404(db, website_id)
        if not website:
            raise WebsiteNotExists()
        website_page: WebsitePage | None = await get_website_page_or_404(db, page_id)
        if not website_page:
            raise WebsitePageNotExists()
        return WebsitePageRead.from_orm(website_page)
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_NOT_FOUND
        )
    except WebsitePageNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.WEBSITE_PAGE_NOT_FOUND
        )
