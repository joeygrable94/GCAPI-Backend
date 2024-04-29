from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonUserClientQueryParams,
    GetUserClientQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_permission_controller,
    get_sharpspring_404,
)
from app.api.exceptions import ClientNotExists, SharpspringAlreadyExists
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
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
from app.crud import ClientRepository, SharpspringRepository
from app.models import Client, Sharpspring
from app.schemas import SharpspringCreate, SharpspringRead, SharpspringUpdate

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="sharpspring:list",
    dependencies=[
        Depends(CommonUserClientQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[SharpspringRead],
)
async def sharpspring_list(
    query: GetUserClientQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[SharpspringRead]:
    """Retrieve a paginated list of sharpspring accounts.

    Permissions:
    ------------
    `role=admin|manager` : all sharpspring accounts

    `role=user` : only sharpspring accounts that belong to the user

    Returns:
    --------
    `Paginated[SharpspringRead]` : a paginated list of sharpspring accounts,
        optionally filtered

    """
    # formulate the select statement based on the current user's role
    ss_repo: SharpspringRepository = SharpspringRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = ss_repo.query_list(client_id=query.client_id)
    else:
        select_stmt = ss_repo.query_list(
            user_id=permissions.current_user.id,
            client_id=query.client_id,
        )
    response_out: Paginated[SharpspringRead] = (
        await permissions.get_paginated_resource_response(
            table_name=Sharpspring.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: SharpspringRead,
                RoleManager: SharpspringRead,
                RoleClient: SharpspringRead,
                RoleEmployee: SharpspringRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="sharpspring:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=SharpspringRead,
)
async def sharpspring_create(
    ss_in: SharpspringCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> SharpspringRead:
    """Create a new sharpspring account.

    Permissions:
    ------------
    `role=admin|manager` : create new sharpspring accounts for all clients

    `role=user` : create only sharpspring accounts that belong to any clients associated
        with the current user

    Returns:
    --------
    `SharpspringRead` : the newly created sharpspring account

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=ss_in.client_id,
    )
    ss_repo: SharpspringRepository = SharpspringRepository(session=permissions.db)
    a_ss: Sharpspring | None = await ss_repo.read_by(
        field_name="api_key",
        field_value=ss_in.api_key,
    )
    if a_ss:
        raise SharpspringAlreadyExists()
    client_repo: ClientRepository = ClientRepository(session=permissions.db)
    a_client: Client | None = await client_repo.read(entry_id=ss_in.client_id)
    if a_client is None:
        raise ClientNotExists()
    new_ss: Sharpspring = await ss_repo.create(ss_in)
    # return role based response
    response_out: SharpspringRead = permissions.get_resource_response(
        resource=new_ss,
        responses={
            RoleUser: SharpspringRead,
        },
    )
    return response_out


@router.get(
    "/{ss_id}",
    name="sharpspring:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_sharpspring_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=SharpspringRead,
)
async def sharpspring_read(
    ss: Sharpspring = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_sharpspring_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> SharpspringRead:
    """Retrieve a single sharpspring account by id.

    Permissions:
    ------------
    `role=admin|manager` : read all sharpspring accounts

    `role=user` : read only sharpspring accounts that belong to any clients
        associated with the current user

    Returns:
    --------
    `SharpspringRead` : the sharpspring account matching the ss_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=ss.client_id,
    )
    # return role based response
    response_out: SharpspringRead = permissions.get_resource_response(
        resource=ss,
        responses={
            RoleUser: SharpspringRead,
        },
    )
    return response_out


@router.patch(
    "/{ss_id}",
    name="sharpspring:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_sharpspring_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=SharpspringRead,
)
async def sharpspring_update(
    ss_in: SharpspringUpdate,
    ss: Sharpspring = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_sharpspring_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> SharpspringRead:
    """Update a sharpspring account by id.

    Permissions:
    ------------
    `role=admin|manager` : update all sharpspring accounts

    `role=user` : update only sharpspring accounts that belong to any clients associated
        with the current user

    Returns:
    --------
    `SharpspringRead` : the updated sharpspring account

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=ss_in,
        schema_privileges={
            RoleUser: SharpspringUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=ss.client_id,
    )
    ss_repo: SharpspringRepository = SharpspringRepository(session=permissions.db)
    if ss_in.api_key is not None:
        a_ss: Sharpspring | None = await ss_repo.read_by(
            field_name="api_key", field_value=ss_in.api_key
        )
        if a_ss:
            raise SharpspringAlreadyExists()
    if ss_in.client_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=ss_in.client_id,
        )
        client_repo: ClientRepository = ClientRepository(session=permissions.db)
        a_client: Client | None = await client_repo.read(entry_id=ss_in.client_id)
        if a_client is None:
            raise ClientNotExists()
    updated_ss: Sharpspring | None = await ss_repo.update(entry=ss, schema=ss_in)
    # return role based response
    response_out: SharpspringRead = permissions.get_resource_response(
        resource=updated_ss if updated_ss else ss,
        responses={
            RoleUser: SharpspringRead,
        },
    )
    return response_out


@router.delete(
    "/{ss_id}",
    name="sharpspring:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_sharpspring_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def sharpspring_delete(
    ss: Sharpspring = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated], get_sharpspring_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a sharpspring account by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any sharpspring accounts

    `role=user` : delete only sharpspring accounts that belong to any clients associated
        with the current user

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=ss.client_id,
    )
    ss_repo: SharpspringRepository = SharpspringRepository(session=permissions.db)
    await ss_repo.delete(entry=ss)
    return None
