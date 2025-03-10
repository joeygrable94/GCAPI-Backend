from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.get_query import (
    CommonOrganizationWebsiteQueryParams,
    GetOrganizationWebsiteQueryParams,
)
from app.core.pagination import PageParams, Paginated
from app.entities.api.dependencies import get_async_db
from app.entities.api.errors import EntityAlreadyExists
from app.entities.auth.dependencies import (
    Permission,
    PermissionController,
    get_current_user,
    get_permission_controller,
)
from app.entities.website.crud import WebsiteRepository
from app.entities.website.dependencies import get_website_or_404
from app.entities.website.errors import DomainInvalid
from app.entities.website.model import Website
from app.entities.website.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate
from app.services.permission import (
    AccessDelete,
    AccessRead,
    AccessUpdate,
    RoleAdmin,
    RoleManager,
    RoleUser,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="websites:list",
    dependencies=[
        Depends(CommonOrganizationWebsiteQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[WebsiteRead],
)
async def website_list(
    query: GetOrganizationWebsiteQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[WebsiteRead]:
    """Retrieve a paginated list of websites.

    Permissions:
    ------------
    `role=admin|manager` : all websites

    `role=user` : only websites associated with the organizations via `organization_website`
        that belong to the user via `user_organization` table

    Returns:
    --------
    `Paginated[WebsiteRead]` : a paginated list of websites, optionally filtered

    """
    websites_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = websites_repo.query_list(organization_id=query.organization_id)
    else:
        select_stmt = websites_repo.query_list(
            organization_id=query.organization_id, user_id=permissions.current_user.id
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
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=WebsiteRead,
)
async def website_create(
    website_in: WebsiteCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> WebsiteRead:
    """Create a new website.

    Permissions:
    ------------
    `role=admin|manager` : create a new website

    Returns:
    --------
    `WebsiteRead` : the newly created website

    """

    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    websites_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    a_site: Website | None = await websites_repo.read_by(
        field_name="domain",
        field_value=website_in.domain,
    )
    if a_site:
        raise EntityAlreadyExists(
            entity_info="Website domain = {}".format(website_in.domain)
        )
    if not await websites_repo.validate(domain=website_in.domain):
        raise DomainInvalid()
    website: Website = await websites_repo.create(website_in)

    response_out: WebsiteRead = permissions.get_resource_response(
        resource=website,
        responses={
            RoleUser: WebsiteRead,
        },
    )
    return response_out


@router.get(
    "/{website_id}",
    name="websites:read",
    dependencies=[
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

    `role=organization` : only websites associated with the organization via `organization_website` table

    `role=user` : only websites associated with organizations they are associated with via
        `user_organization` table, and associated with the organization via `organization_website` table

    Returns:
    --------
    `WebsiteRead` : the website matching the website_id

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=website.id,
    )

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

    `role=organization` : only websites associated with the organization via `organization_website` table

    `role=user` : only websites associated with organizations they are associated with via
        `user_organization` table, and associated with the organization via `organization_website` table

    Returns:
    --------
    `WebsiteRead` : the updated website

    """
    permissions.verify_input_schema_by_role(
        input_object=website_in,
        schema_privileges={
            RoleUser: WebsiteUpdate,
        },
    )
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
            raise EntityAlreadyExists(
                entity_info="Website domain = {}".format(website_in.domain)
            )
        if not await websites_repo.validate(domain=website_in.domain):
            raise DomainInvalid()
    updated_website: Website | None = await websites_repo.update(
        entry=website, schema=website_in
    )

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

    `role=organization` : only websites associated with the organization via `organization_website` table

    `role=user` : only websites associated with organizations they are associated with via
        `user_organization` table, and associated with the organization via `organization_website` table

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
