from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CommonWebsiteMapQueryParams,
    CurrentUser,
    FetchSitemapOr404,
    GetWebsiteMapQueryParams,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_website_map_or_404,
)
from app.api.exceptions import WebsiteMapAlreadyExists, WebsiteNotExists
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
)
from app.crud import WebsiteMapRepository, WebsiteRepository
from app.models import Website, WebsiteMap
from app.schemas import (
    WebsiteMapCreate,
    WebsiteMapProcessing,
    WebsiteMapRead,
    WebsiteMapUpdate,
)
from app.worker import task_website_sitemap_fetch_pages

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="website_sitemaps:list",
    dependencies=[
        Depends(CommonWebsiteMapQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[WebsiteMapRead],
)
async def sitemap_list(
    query: GetWebsiteMapQueryParams,
    db: AsyncDatabaseSession,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsiteMapRead]:
    """Retrieve a paginated list of website maps.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=client` : only website maps with a website_id associated with the client
        via `client_website` table

    `role=employee` : only website maps with a website_id associated with the clients
        via `client_website` table, associated with the user via `user_client` table

    Returns:
    --------
    `Paginated[WebsiteMapRead]` : a paginated list of website maps,
        optionally filtered

    """
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
    response_out: Paginated[
        WebsiteMapRead
    ] = await permissions.get_paginated_resource_response(
        table_name=WebsiteMap.__tablename__,
        stmt=sitemap_repo.query_list(website_id=query.website_id),
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleAdmin: WebsiteMapRead,
            RoleManager: WebsiteMapRead,
            RoleClient: WebsiteMapRead,
            RoleEmployee: WebsiteMapRead,
        },
    )
    return response_out


@router.post(
    "/",
    name="website_sitemaps:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=WebsiteMapRead,
)
async def sitemap_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    sitemap_in: WebsiteMapCreate,
) -> WebsiteMapRead:
    """Create a new website map.

    Permissions:
    ------------
    `role=admin|manager` : create a new website map

    `role=client` : create a new website map that belongs to a website associated with
        the client via `client_website` table

    `role=employee` : create a new website map associated with a website that belongs to
        a client the user belongs to via `user_client` table

    Returns:
    --------
    `WebsiteMapRead` : the newly created website map

    """
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
    return WebsiteMapRead.model_validate(sitemap)


@router.get(
    "/{sitemap_id}",
    name="website_sitemaps:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_map_or_404),
    ],
    response_model=WebsiteMapRead,
)
async def sitemap_read(
    current_user: CurrentUser,
    sitemap: FetchSitemapOr404,
) -> WebsiteMapRead:
    """Retrieve a single website map by id.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=client` : only website maps belonging to a website associated with the client

    `role=employee` : only website maps belonging to a website that belongs to a client
        the user is associated with to via `user_client` table

    Returns:
    --------
    `WebsiteMapRead` : the website map

    """
    return WebsiteMapRead.model_validate(sitemap)


@router.patch(
    "/{sitemap_id}",
    name="website_sitemaps:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_map_or_404),
    ],
    response_model=WebsiteMapRead,
)
async def sitemap_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    sitemap: FetchSitemapOr404,
    sitemap_in: WebsiteMapUpdate,
) -> WebsiteMapRead:
    """Update a website map by id.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=client` : only website maps belonging to a website associated with the client

    `role=employee` : only website maps belonging to a website that belongs to a client
        the user is associated with to via `user_client` table

    Returns:
    --------
    `WebsiteMapRead` : the updated website map

    """
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
    updated_sitemap: WebsiteMap | None = await sitemap_repo.update(
        entry=sitemap, schema=sitemap_in
    )
    return (
        WebsiteMapRead.model_validate(updated_sitemap)
        if updated_sitemap
        else WebsiteMapRead.model_validate(sitemap)
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
    """Delete a website map by id.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=client` : only website maps belonging to a website associated with the client

    `role=employee` : only website maps belonging to a website that belongs to a client
        the user is associated with to via `user_client` table

    Returns:
    --------
    `None`

    """
    sitemap_repo: WebsiteMapRepository = WebsiteMapRepository(session=db)
    await sitemap_repo.delete(entry=sitemap)
    return None


@router.get(
    "/{sitemap_id}/process-pages",
    name="website_sitemaps:process_sitemap_pages",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_map_or_404),
    ],
    response_model=WebsiteMapProcessing,
)
async def sitemap_process_sitemap_pages(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    sitemap: FetchSitemapOr404,
) -> WebsiteMapProcessing:
    """A webhook to initiate processing a sitemap's pages.

    Permissions:
    ------------
    `role=admin|manager` : all website maps

    `role=client` : only website maps belonging to a website associated with the client

    `role=employee` : only website maps belonging to a website that belongs to a client
        the user is associated with to via `user_client` table

    Returns:
    --------
    `WebsiteMapProcessing` : the task_id of the worker task

    """
    website_map_processing_pages: Any = task_website_sitemap_fetch_pages.delay(
        website_id=sitemap.website_id, sitemap_url=sitemap.url
    )
    return WebsiteMapProcessing(
        url=sitemap.url,
        website_id=sitemap.website_id,
        task_id=website_map_processing_pages.task_id,
    )
