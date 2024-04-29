from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonClientQueryParams,
    GetClientQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_go_cloud_404,
    get_permission_controller,
)
from app.api.exceptions import ClientNotExists, GoCloudPropertyAlreadyExists
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
from app.crud import ClientRepository, GoCloudPropertyRepository
from app.models import Client, GoCloudProperty
from app.schemas import (
    GoCloudPropertyCreate,
    GoCloudPropertyRead,
    GoCloudPropertyUpdate,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="go_cloud_property:list",
    dependencies=[
        Depends(CommonClientQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[GoCloudPropertyRead],
)
async def go_cloud_property_list(
    query: GetClientQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[GoCloudPropertyRead]:
    """Retrieve a paginated list of go_cloud property.

    Permissions:
    ------------
    `role=admin|manager` : all go_cloud properties

    `role=user` : only go_cloud properties that belong to the user

    Returns:
    --------
    `Paginated[GoCloudPropertyRead]` : a paginated list of go_cloud properties,
        optionally filtered

    """
    # formulate the select statement based on the current user's role
    go_cloud_repo: GoCloudPropertyRepository = GoCloudPropertyRepository(
        session=permissions.db
    )
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = go_cloud_repo.query_list(client_id=query.client_id)
    else:
        select_stmt = go_cloud_repo.query_list(
            user_id=permissions.current_user.id,
            client_id=query.client_id,
        )
    response_out: Paginated[GoCloudPropertyRead] = (
        await permissions.get_paginated_resource_response(
            table_name=GoCloudProperty.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: GoCloudPropertyRead,
                RoleManager: GoCloudPropertyRead,
                RoleClient: GoCloudPropertyRead,
                RoleEmployee: GoCloudPropertyRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="go_cloud_property:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoCloudPropertyRead,
)
async def go_cloud_property_create(
    go_cloud_in: GoCloudPropertyCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoCloudPropertyRead:
    """Create a new go_cloud property.

    Permissions:
    ------------
    `role=admin|manager` : create new go_cloud properties for all clients

    `role=user` : create only go_cloud properties that belong to any clients associated
        with the current user

    Returns:
    --------
    `GoCloudPropertyRead` : the newly created go_cloud

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_cloud_in.client_id,
    )
    go_cloud_repo: GoCloudPropertyRepository = GoCloudPropertyRepository(
        session=permissions.db
    )
    agc_project_name: GoCloudProperty | None = await go_cloud_repo.read_by(
        field_name="project_name",
        field_value=go_cloud_in.project_name,
    )
    agc_project_id: GoCloudProperty | None = await go_cloud_repo.read_by(
        field_name="project_id",
        field_value=go_cloud_in.project_id,
    )
    agc_project_number: GoCloudProperty | None = await go_cloud_repo.read_by(
        field_name="project_number",
        field_value=go_cloud_in.project_number,
    )
    agc_service_account: GoCloudProperty | None = None
    if go_cloud_in.service_account:
        agc_service_account = await go_cloud_repo.read_by(
            field_name="service_account",
            field_value=go_cloud_in.service_account,
        )
    if (
        agc_project_name is not None
        or agc_project_id is not None
        or agc_project_number is not None
        or agc_service_account is not None
    ):
        raise GoCloudPropertyAlreadyExists()
    client_repo: ClientRepository = ClientRepository(session=permissions.db)
    a_client: Client | None = await client_repo.read(entry_id=go_cloud_in.client_id)
    if a_client is None:
        raise ClientNotExists()
    new_go_cloud: GoCloudProperty = await go_cloud_repo.create(go_cloud_in)
    # return role based response
    response_out: GoCloudPropertyRead = permissions.get_resource_response(
        resource=new_go_cloud,
        responses={
            RoleUser: GoCloudPropertyRead,
        },
    )
    return response_out


@router.get(
    "/{go_cloud_id}",
    name="go_cloud_property:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_go_cloud_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoCloudPropertyRead,
)
async def go_cloud_property_read(
    go_cloud: GoCloudProperty = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_go_cloud_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoCloudPropertyRead:
    """Retrieve a single go_cloud property by id.

    Permissions:
    ------------
    `role=admin|manager` : read all go_cloud properties

    `role=user` : read only go_cloud properties that belong to any clients
        associated with the current user

    Returns:
    --------
    `GoCloudPropertyRead` : the go_cloud matching the go_cloud_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_cloud.client_id,
    )
    # return role based response
    response_out: GoCloudPropertyRead = permissions.get_resource_response(
        resource=go_cloud,
        responses={
            RoleUser: GoCloudPropertyRead,
        },
    )
    return response_out


@router.patch(
    "/{go_cloud_id}",
    name="go_cloud_property:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_go_cloud_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoCloudPropertyRead,
)
async def go_cloud_property_update(
    go_cloud_in: GoCloudPropertyUpdate,
    go_cloud: GoCloudProperty = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_go_cloud_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoCloudPropertyRead:
    """Update a go_cloud by id.

    Permissions:
    ------------
    `role=admin|manager` : update all go_cloud properties

    `role=user` : update only go_cloud properties that belong to any clients associated
        with the current user

    Returns:
    --------
    `GoCloudPropertyRead` : the updated go_cloud property

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=go_cloud_in,
        schema_privileges={
            RoleUser: GoCloudPropertyUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_cloud.client_id,
    )
    go_cloud_repo: GoCloudPropertyRepository = GoCloudPropertyRepository(
        session=permissions.db
    )
    if go_cloud_in.project_name is not None:
        a_go_cloud: GoCloudProperty | None = await go_cloud_repo.read_by(
            field_name="project_name", field_value=go_cloud_in.project_name
        )
        if a_go_cloud is not None:
            raise GoCloudPropertyAlreadyExists()
    if go_cloud_in.service_account:
        b_go_cloud: GoCloudProperty | None = await go_cloud_repo.read_by(
            field_name="service_account",
            field_value=go_cloud_in.service_account,
        )
        if b_go_cloud is not None:
            raise GoCloudPropertyAlreadyExists()
    if go_cloud_in.client_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=go_cloud_in.client_id,
        )
        client_repo: ClientRepository = ClientRepository(session=permissions.db)
        a_client: Client | None = await client_repo.read(entry_id=go_cloud_in.client_id)
        if a_client is None:
            raise ClientNotExists()
    updated_go_cloud: GoCloudProperty | None = await go_cloud_repo.update(
        entry=go_cloud, schema=go_cloud_in
    )
    # return role based response
    response_out: GoCloudPropertyRead = permissions.get_resource_response(
        resource=updated_go_cloud if updated_go_cloud else go_cloud,
        responses={
            RoleUser: GoCloudPropertyRead,
        },
    )
    return response_out


@router.delete(
    "/{go_cloud_id}",
    name="go_cloud_property:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_go_cloud_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def go_cloud_property_delete(
    go_cloud: GoCloudProperty = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated], get_go_cloud_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a go_cloud property by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any go_cloud properties

    `role=user` : delete only go_cloud properties that belong to any clients associated
        with the current user

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_cloud.client_id,
    )
    go_cloud_repo: GoCloudPropertyRepository = GoCloudPropertyRepository(
        session=permissions.db
    )
    await go_cloud_repo.delete(entry=go_cloud)
    return None
