from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchWebsiteOr404,
    GetClientWebsiteQueryParams,
    get_async_db,
    get_website_or_404,
)
from app.api.errors import ErrorCode
from app.api.exceptions import WebsiteAlreadyExists, WebsiteDomainInvalid
from app.core.auth import auth
from app.crud import WebsiteRepository
from app.models import Website
from app.schemas import (
    WebsiteCreate,
    WebsiteCreateProcessing,
    WebsiteRead,
    WebsiteReadRelations,
    WebsiteUpdate,
)
from app.worker import task_website_sitemap_fetch_pages

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="websites:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[WebsiteReadRelations],
)
async def website_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetClientWebsiteQueryParams,
) -> List[WebsiteRead] | List:
    websites_repo: WebsiteRepository = WebsiteRepository(session=db)
    websites: List[Website] | List[None] | None = await websites_repo.list(
        page=query.page
    )
    return [WebsiteRead.from_orm(w) for w in websites] if websites else []


@router.post(
    "/",
    name="websites:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=WebsiteCreateProcessing,
)
async def website_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website_in: WebsiteCreate,
) -> WebsiteCreateProcessing:
    try:
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        a_site: Website | None = await websites_repo.read_by(
            field_name="domain",
            field_value=website_in.domain,
        )
        if a_site:
            raise WebsiteAlreadyExists()
        if not await websites_repo.validate(domain=website_in.domain):
            raise WebsiteDomainInvalid()
        new_site: Website = await websites_repo.create(website_in)
        sitemap_task = task_website_sitemap_fetch_pages.delay(
            website_id=new_site.id, sitemap_url=new_site.get_link()
        )
        return WebsiteCreateProcessing(
            website=WebsiteRead.from_orm(new_site), task_id=sitemap_task.id
        )
    except WebsiteDomainInvalid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.WEBSITE_DOMAIN_INVALID,
        )
    except WebsiteAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.WEBSITE_DOMAIN_EXISTS,
        )


@router.get(
    "/{website_id}",
    name="websites:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_or_404),
    ],
    response_model=WebsiteReadRelations,
)
async def website_read(
    current_user: CurrentUser,
    website: FetchWebsiteOr404,
) -> WebsiteRead:
    return WebsiteRead.from_orm(website)


@router.patch(
    "/{website_id}",
    name="websites:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_or_404),
    ],
    response_model=WebsiteReadRelations,
)
async def website_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website: FetchWebsiteOr404,
    website_in: WebsiteUpdate,
) -> WebsiteRead:
    try:
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        if website_in.domain is not None:
            domain_found: Website | None = await websites_repo.read_by(
                field_name="domain",
                field_value=website_in.domain,
            )
            if domain_found:
                raise WebsiteAlreadyExists()
        updated_website: Website | None = await websites_repo.update(
            entry=website, schema=website_in
        )
        return (
            WebsiteRead.from_orm(updated_website)
            if updated_website
            else WebsiteRead.from_orm(website)
        )
    except WebsiteAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.WEBSITE_DOMAIN_EXISTS,
        )


@router.delete(
    "/{website_id}",
    name="websites:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_or_404),
    ],
    response_model=None,
)
async def website_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website: FetchWebsiteOr404,
) -> None:
    websites_repo: WebsiteRepository = WebsiteRepository(session=db)
    await websites_repo.delete(entry=website)
    return None
