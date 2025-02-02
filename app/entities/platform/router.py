from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.get_query import (
    CommonClientPlatformQueryParams,
    GetClientPlatformQueryParams,
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
from app.entities.platform.crud import PlatformRepository
from app.entities.platform.dependencies import get_platform_404
from app.entities.platform.model import Platform
from app.entities.platform.schemas import (
    PlatformCreate,
    PlatformRead,
    PlatformUpdate,
    PlatformUpdateAsAdmin,
    PlatformUpdateAsManager,
)
from app.services.permission import (
    AccessDelete,
    AccessDeleteRelated,
    AccessDeleteSelf,
    AccessRead,
    AccessReadRelated,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateRelated,
    AccessUpdateSelf,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="platform:list",
    dependencies=[
        Depends(CommonClientPlatformQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[PlatformRead],
)
async def platform_list(
    query: GetClientPlatformQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[PlatformRead]:
    """Retrieve a paginated list of platforms.

    Permissions:
    ------------
    `role=admin|manager` : all platforms

    `role=user` : only platforms associated with the user via `user_client`
        table and associated with the client via `client_platform` table

    Returns:
    --------
    `Paginated[PlatformRead]` : a paginated list of platforms,
        optionally filtered

    """
    platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = platform_repo.query_list(
            client_id=query.client_id, is_active=query.is_active
        )
    else:
        select_stmt = platform_repo.query_list(
            user_id=permissions.current_user.id,
            client_id=query.client_id,
            is_active=query.is_active,
        )
    response_out: Paginated[
        PlatformRead
    ] = await permissions.get_paginated_resource_response(
        table_name=Platform.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleAdmin: PlatformRead,
            RoleManager: PlatformRead,
            RoleClient: PlatformRead,
            RoleEmployee: PlatformRead,
        },
    )
    return response_out


@router.post(
    "/",
    name="platform:create",
    dependencies=[
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=PlatformRead,
)
async def platform_create(
    platform_in: PlatformCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> PlatformRead:
    """Create a new platform account.

    Permissions:
    ------------
    `role=admin|manager` : create new platforms for all clients

    Returns:
    --------
    `PlatformRead` : the newly created platform account

    """
    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
    a_platform: Platform | None = await platform_repo.read_by(
        field_name="slug",
        field_value=platform_in.slug,
    )
    if a_platform:
        raise EntityAlreadyExists(
            entity_info="Platform slug = {}".format(platform_in.slug)
        )
    a_platform: Platform | None = await platform_repo.read_by(
        field_name="title",
        field_value=platform_in.title,
    )
    if a_platform:
        raise EntityAlreadyExists(
            entity_info="Platform title = {}".format(platform_in.title)
        )
    new_platform: Platform = await platform_repo.create(platform_in)
    response_out: PlatformRead = permissions.get_resource_response(
        resource=new_platform,
        responses={
            RoleUser: PlatformRead,
        },
    )
    return response_out


@router.get(
    "/{platform_id}",
    name="platform:read",
    dependencies=[
        Depends(get_async_db),
        Depends(get_platform_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=PlatformRead,
)
async def platform_read(
    platform: Platform = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_platform_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> PlatformRead:
    """Retrieve a single platform account by id.

    Permissions:
    ------------
    `role=admin|manager` : read all platforms

    `role=user` : only platforms associated with clients they are associated with via
        `user_client` table, and associated with the client via `client_platform` table

    Returns:
    --------
    `PlatformRead` : the platform account matching the platform_id

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        platform_id=platform.id,
    )
    response_out: PlatformRead = permissions.get_resource_response(
        resource=platform,
        responses={
            RoleUser: PlatformRead,
        },
    )
    return response_out


@router.patch(
    "/{platform_id}",
    name="platform:update",
    dependencies=[
        Depends(get_async_db),
        Depends(get_platform_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=PlatformRead,
)
async def platform_update(
    platform_in: PlatformUpdateAsAdmin | PlatformUpdateAsManager | PlatformUpdate,
    platform: Platform = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_platform_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> PlatformRead:
    """Update a platform account by id.

    Permissions:
    ------------
    `role=admin` : all users, all fields

    `role=manager` : all users, limited fields

    `role=user` : limited fields, only platforms associated with clients they are associated with via
        `user_client` table, and associated with the client via `client_platform` table

    Returns:
    --------
    `PlatformRead` : the updated platform account

    """
    permissions.verify_input_schema_by_role(
        input_object=platform_in,
        schema_privileges={
            RoleAdmin: PlatformUpdateAsAdmin,
            RoleManager: PlatformUpdateAsManager,
            RoleUser: PlatformUpdate,
        },
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        platform_id=platform.id,
    )
    platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
    if platform_in.title is not None:
        a_platform: Platform | None = await platform_repo.read_by(
            field_name="title", field_value=platform_in.title
        )
        if a_platform:
            raise EntityAlreadyExists(
                entity_info="Platform title = {}".format(platform_in.title)
            )
    updated_platform: Platform | None = await platform_repo.update(
        entry=platform, schema=platform_in
    )
    if updated_platform is None:  # pragma: no cover
        updated_platform = platform
    response_out: PlatformRead = permissions.get_resource_response(
        resource=updated_platform,
        responses={
            RoleAdmin: PlatformRead,
            RoleManager: PlatformRead,
            RoleUser: PlatformRead,
        },
    )
    return response_out


@router.delete(
    "/{platform_id}",
    name="platform:delete",
    dependencies=[
        Depends(get_async_db),
        Depends(get_platform_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def platform_delete(
    platform: Platform = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated], get_platform_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a platform account by id.

    Permissions:
    ------------
    `role=admin` : delete any platforms

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(privileges=[RoleAdmin])
    platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
    await platform_repo.delete(entry=platform)
    return None
