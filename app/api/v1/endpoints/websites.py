from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonClientWebsiteQueryParams,
    GetClientWebsiteQueryParams,
    Permission,
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
    AccessDelete,
    AccessRead,
    AccessUpdate,
    RoleAdmin,
    RoleManager,
    RoleUser,
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
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsiteRead]:
    """Retrieve a paginated list of websites.

    Permissions:
    ------------
    `role=admin|manager` : all websites

    `role=user` : only websites associated with the clients via `client_website`
        that belong to the user via `user_client` table

    Returns:
    --------
    `Paginated[WebsiteRead]` : a paginated list of websites, optionally filtered

    """
    websites_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = websites_repo.query_list(client_id=query.client_id)
    else:  # TODO: test
        select_stmt = websites_repo.query_list(
            client_id=query.client_id, user_id=permissions.current_user.id
        )
    response_out: Paginated[
        WebsiteRead
    ] = await permissions.get_paginated_resource_response(
        table_name=Website.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleUser: WebsiteRead,
        },
    )
    return response_out


@router.post(
    "/",
    name="websites:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteCreateProcessing,
)
async def website_create(
    website_in: WebsiteCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsiteCreateProcessing:
    """Create a new website.

    Permissions:
    ------------
    `role=admin|manager` : create a new website

    Returns:
    --------
    `WebsiteCreateProcessing` : the newly created website and the task id for the
        background task that will fetch the sitemap pages

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    websites_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
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
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteRead,
)
async def website_read(
    website: Website = Permission(AccessRead, get_website_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
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
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website.id,
    )
    # return role based response
    response_out: WebsiteRead = permissions.get_resource_response(
        resource=website,
        responses={
            RoleUser: WebsiteRead,
        },
    )
    return response_out


@router.patch(
    "/{website_id}",
    name="websites:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteRead,
)
async def website_update(
    website_in: WebsiteUpdate,
    website: Website = Permission(AccessUpdate, get_website_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
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
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=website_in,
        schema_privileges={
            RoleUser: WebsiteUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website.id,
    )
    websites_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
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
    # return role based response
    response_out: WebsiteRead = permissions.get_resource_response(
        resource=updated_website if updated_website else website,
        responses={
            RoleUser: WebsiteRead,
        },
    )
    return response_out


@router.delete(
    "/{website_id}",
    name="websites:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_website_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def website_delete(
    website: Website = Permission(AccessDelete, get_website_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a website by id.

    Permissions:
    ------------
    `role=admin|manager` : all websites

    `role=client` : only websites associated with the client via `client_website` table

    `role=employee` : only websites associated with clients they are associated with via
        `user_client` table, and associated with the client via `client_website` table

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], website_id=website.id
    )
    websites_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    await websites_repo.delete(entry=website)
    return None
