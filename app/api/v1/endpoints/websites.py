from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CommonClientWebsiteQueryParams,
    CurrentUser,
    FetchWebsiteOr404,
    GetClientWebsiteQueryParams,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_website_or_404,
)
from app.api.exceptions import WebsiteAlreadyExists, WebsiteDomainInvalid
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
)
from app.crud import WebsiteRepository
from app.models import Website
from app.schemas import (
    WebsiteCreate,
    WebsiteCreateProcessing,
    WebsiteRead,
    WebsiteUpdate,
)
from app.worker import task_website_sitemap_fetch_pages

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="websites:list",
    dependencies=[
        Depends(CommonClientWebsiteQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[WebsiteRead],
)
async def website_list(
    query: GetClientWebsiteQueryParams,
    db: AsyncDatabaseSession,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsiteRead]:
    """Retrieve a paginated list of websites.

    Permissions:
    ------------
    `role=admin|manager` : all websites

    `role=client` : only websites associated with the client via `client_website` table

    `role=employee` : only websites associated with the clients via `client_website`
        that belong to the user via `user_client` table

    Returns:
    --------
    `Paginated[WebsiteRead]` : a paginated list of websites, optionally filtered

    """
    websites_repo: WebsiteRepository = WebsiteRepository(session=db)
    response_out: Paginated[
        WebsiteRead
    ] = await permissions.get_paginated_resource_response(
        table_name=Website.__tablename__,
        stmt=websites_repo.query_list(),
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleAdmin: WebsiteRead,
            RoleManager: WebsiteRead,
            RoleClient: WebsiteRead,
            RoleEmployee: WebsiteRead,
        },
    )
    return response_out


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
    """Create a new website.

    Permissions:
    ------------
    `role=admin|manager` : create a new website

    `role=client` : create a new website associated with the client via `client_website`

    `role=employee` : create a new website only for clients associated with the user via
        `user_client` table, and associated with the client via `client_website` table

    Returns:
    --------
    `WebsiteCreateProcessing` : the newly created website and the task id for the
        background task that will fetch the sitemap pages

    """
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
    a_sitemap_url = new_site.get_link()
    sitemap_task = task_website_sitemap_fetch_pages.delay(new_site.id, a_sitemap_url)
    return WebsiteCreateProcessing(
        website=WebsiteRead.model_validate(new_site), task_id=sitemap_task.task_id
    )


@router.get(
    "/{website_id}",
    name="websites:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_or_404),
    ],
    response_model=WebsiteRead,
)
async def website_read(
    current_user: CurrentUser,
    website: FetchWebsiteOr404,
) -> WebsiteRead:
    """Retrieve a single website by id.

    Permissions:
    ------------
    `role=admin|manager` : all websites

    `role=client` : only websites associated with the client via `client_website` table

    `role=employee` : only websites associated with clients they are associated with via
        `user_client` table, and associated with the client via `client_website` table

    Returns:
    --------
    `WebsiteRead` : the website matching the website_id

    """
    return WebsiteRead.model_validate(website)


@router.patch(
    "/{website_id}",
    name="websites:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_or_404),
    ],
    response_model=WebsiteRead,
)
async def website_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    website: FetchWebsiteOr404,
    website_in: WebsiteUpdate,
) -> WebsiteRead:
    """Update a website by id.

    Permissions:
    ------------
    `role=admin|manager` : all websites

    `role=client` : only websites associated with the client via `client_website` table

    `role=employee` : only websites associated with clients they are associated with via
        `user_client` table, and associated with the client via `client_website` table

    Returns:
    --------
    `WebsiteRead` : the updated website

    """
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
        WebsiteRead.model_validate(updated_website)
        if updated_website
        else WebsiteRead.model_validate(website)
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
    """Delete a website by id.

    Permissions:
    ------------
    `role=admin|manager` : all websites

    Returns:
    --------
    `None`

    """
    websites_repo: WebsiteRepository = WebsiteRepository(session=db)
    await websites_repo.delete(entry=website)
    return None
