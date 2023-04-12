from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchWebPageOr404,
    GetWebsitePageQueryParams,
    get_async_db,
    get_website_page_or_404,
)
from app.api.errors import ErrorCode
from app.api.exceptions import (
    WebsiteNotExists,
    WebsitePageAlreadyExists,
    WebsitePageNotExists,
)
from app.core.auth import auth
from app.crud import WebsitePageRepository, WebsiteRepository
from app.models import Website, WebsitePage
from app.schemas import (
    WebsitePageCreate,
    WebsitePageFetchPSIProcessing,
    WebsitePageRead,
    WebsitePageReadRelations,
    WebsitePageUpdate,
)
from app.worker import task_website_page_pagespeedinsights_fetch

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_pages:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[WebsitePageReadRelations],
)
async def website_page_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetWebsitePageQueryParams,
) -> List[WebsitePageRead] | List:
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
    website_list: List[WebsitePage] | List[None] | None = await web_pages_repo.list(
        page=query.page,
        website_id=query.website_id,
        sitemap_id=query.sitemap_id,
    )
    return [WebsitePageRead.from_orm(w) for w in website_list] if len(website_list) else []


@router.post(
    "/",
    name="website_pages:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=WebsitePageFetchPSIProcessing,
)
async def website_page_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website_page_in: WebsitePageCreate,
) -> WebsitePageFetchPSIProcessing:
    try:
        website_repo: WebsiteRepository = WebsiteRepository(session=db)
        web_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
        # check website page url is unique to website_id
        a_page: WebsitePage | None = await web_pages_repo.exists_by_two(
            field_name_a="url",
            field_value_a=website_page_in.url,
            field_name_b="website_id",
            field_value_b=website_page_in.website_id,
        )
        if a_page is not None:
            raise WebsitePageAlreadyExists()
        # check website page is assigned to a website
        website_page: WebsitePage = await web_pages_repo.create(website_page_in)
        a_website: Website | None = await website_repo.read(website_page_in.website_id)
        if a_website is None:
            raise WebsiteNotExists()
        fetch_page = a_website.get_link() + website_page.url
        website_page_psi_mobile = task_website_page_pagespeedinsights_fetch.delay(
            website_id=a_website.id,
            page_id=website_page.id,
            fetch_psi_url=fetch_page,
            device="mobile",
        )
        website_page_psi_desktop = task_website_page_pagespeedinsights_fetch.delay(
            website_id=a_website.id,
            page_id=website_page.id,
            fetch_psi_url=fetch_page,
            device="desktop",
        )
        return WebsitePageFetchPSIProcessing(
            page=WebsitePageRead.from_orm(website_page),
            mobile_task_id=website_page_psi_mobile.id,
            desktop_task_id=website_page_psi_desktop.id,
        )
    except WebsiteNotExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.WEBSITE_PAGE_UNASSIGNED_WEBSITE_ID,
        )
    except WebsitePageAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.WEBSITE_PAGE_URL_EXISTS,
        )


@router.get(
    "/{page_id}",
    name="website_pages:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_or_404),
    ],
    response_model=WebsitePageReadRelations,
)
async def website_page_read(
    current_user: CurrentUser,
    website_page: FetchWebPageOr404,
) -> WebsitePageRead:
    return WebsitePageRead.from_orm(website_page)


@router.patch(
    "/{page_id}",
    name="website_pages:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_or_404),
    ],
    response_model=WebsitePageReadRelations,
)
async def website_page_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website_page: FetchWebPageOr404,
    website_page_in: WebsitePageUpdate,
) -> WebsitePageRead:
    try:
        web_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
        updated_website_page: WebsitePage | None = await web_pages_repo.update(
            entry=website_page, schema=website_page_in
        )
        return WebsitePageRead.from_orm(updated_website_page) if updated_website_page else WebsitePageRead.from_orm(website_page)
    except WebsitePageNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_PAGE_NOT_FOUND,
        )


@router.delete(
    "/{page_id}",
    name="website_pages:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_page_or_404),
    ],
    response_model=None,
)
async def website_page_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website_page: FetchWebPageOr404,
) -> None:
    web_pages_repo: WebsitePageRepository = WebsitePageRepository(session=db)
    await web_pages_repo.delete(entry=website_page)
    return None
