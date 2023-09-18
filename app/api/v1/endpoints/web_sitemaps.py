from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchSitemapOr404,
    GetWebsiteMapQueryParams,
    get_async_db,
    get_website_map_or_404,
)
from app.api.errors import ErrorCode
from app.api.exceptions import WebsiteMapAlreadyExists, WebsiteNotExists
from app.core.auth import auth
from app.crud import WebsiteMapRepository, WebsiteRepository
from app.models import Website, WebsiteMap
from app.schemas import (
    WebsiteMapCreate,
    WebsiteMapProcessing,
    WebsiteMapRead,
    WebsiteMapReadRelations,
    WebsiteMapUpdate,
)
from app.worker import task_website_sitemap_fetch_pages

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_sitemaps:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[WebsiteMapReadRelations],
)
async def sitemap_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsiteMapQueryParams,
) -> List[WebsiteMapRead] | List:
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
    sitemaps: List[WebsiteMap] | List[None] | None = await sitemap_repo.list(
        page=query.page,
        website_id=query.website_id,
    )
    return [WebsiteMapRead.from_orm(w) for w in sitemaps] if sitemaps else []


@router.post(
    "/",
    name="website_sitemaps:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=WebsiteMapReadRelations,
)
async def sitemap_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    sitemap_in: WebsiteMapCreate,
) -> WebsiteMapRead:
    try:
        sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
        # check website map url is unique to website_id
        a_sitemap: WebsiteMap | None = await sitemap_repo.exists_by_two(
            field_name_a="url",
            field_value_a=sitemap_in.url,
            field_name_b="website_id",
            field_value_b=sitemap_in.website_id,
        )
        if a_sitemap is not None:
            raise WebsiteMapAlreadyExists()
        # check website map is assigned to a website
        website_repo: WebsiteRepository = WebsiteRepository(session=db)
        a_website: Website | None = await website_repo.read(sitemap_in.website_id)
        if a_website is None:
            raise WebsiteNotExists()
        # create website map
        sitemap: WebsiteMap = await sitemap_repo.create(sitemap_in)
        return WebsiteMapRead.from_orm(sitemap)
    except WebsiteNotExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.WEBSITE_MAP_UNASSIGNED_WEBSITE_ID,
        )
    except WebsiteMapAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.WEBSITE_MAP_EXISTS,
        )


@router.get(
    "/{sitemap_id}",
    name="website_sitemaps:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_map_or_404),
    ],
    response_model=WebsiteMapReadRelations,
)
async def sitemap_read(
    current_user: CurrentUser,
    sitemap: FetchSitemapOr404,
) -> WebsiteMapRead:
    return WebsiteMapRead.from_orm(sitemap)


@router.patch(
    "/{sitemap_id}",
    name="website_sitemaps:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_map_or_404),
    ],
    response_model=WebsiteMapReadRelations,
)
async def sitemap_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    sitemap: FetchSitemapOr404,
    sitemap_in: WebsiteMapUpdate,
) -> WebsiteMapRead:
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
    updated_sitemap: WebsiteMap | None = await sitemap_repo.update(
        entry=sitemap, schema=sitemap_in
    )
    return (
        WebsiteMapRead.from_orm(updated_sitemap)
        if updated_sitemap
        else WebsiteMapRead.from_orm(sitemap)
    )


@router.delete(
    "/{sitemap_id}",
    name="website_sitemaps:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_map_or_404),
    ],
    response_model=None,
)
async def sitemap_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    sitemap: FetchSitemapOr404,
) -> None:
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
    await sitemap_repo.delete(entry=sitemap)
    return None


@router.post(
    "/{sitemap_id}",
    name="website_sitemaps:process_pages",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_map_or_404),
    ],
    response_model=WebsiteMapReadRelations,
)
async def sitemap_process_pages(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    sitemap: FetchSitemapOr404,
) -> WebsiteMapProcessing:
    website_map_processing_pages: Any = task_website_sitemap_fetch_pages.delay(
        website_id=sitemap.website_id, sitemap_url=sitemap.url
    )
    return WebsiteMapProcessing(
        url=sitemap.url,
        website_id=sitemap.website_id,
        task_id=website_map_processing_pages.id,
    )
