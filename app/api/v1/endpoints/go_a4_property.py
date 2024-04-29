from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonClientQueryParams,
    GetClientQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_ga4_property_404,
    get_permission_controller,
)
from app.api.exceptions import ClientNotExists, Ga4PropertyAlreadyExists
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
from app.crud import ClientRepository, GoAnalytics4PropertyRepository
from app.models import Client, GoAnalytics4Property
from app.schemas import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
    GoAnalytics4PropertyUpdate,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="ga4_property:list",
    dependencies=[
        Depends(CommonClientQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[GoAnalytics4PropertyRead],
)
async def ga4_property_list(
    query: GetClientQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[GoAnalytics4PropertyRead]:
    """Retrieve a paginated list of ga4 properties.

    Permissions:
    ------------
    `role=admin|manager` : all ga4 properties

    `role=user` : only ga4 properties that belong to the user

    Returns:
    --------
    `Paginated[GoAnalytics4PropertyRead]` : a paginated list of ga4 properties,
        optionally filtered

    """
    # formulate the select statement based on the current user's role
    ga4_repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=permissions.db
    )
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = ga4_repo.query_list(client_id=query.client_id)
    else:
        select_stmt = ga4_repo.query_list(
            user_id=permissions.current_user.id,
            client_id=query.client_id,
        )
    response_out: Paginated[GoAnalytics4PropertyRead] = (
        await permissions.get_paginated_resource_response(
            table_name=GoAnalytics4Property.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: GoAnalytics4PropertyRead,
                RoleManager: GoAnalytics4PropertyRead,
                RoleClient: GoAnalytics4PropertyRead,
                RoleEmployee: GoAnalytics4PropertyRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="ga4_property:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4PropertyRead,
)
async def ga4_property_create(
    ga4_in: GoAnalytics4PropertyCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoAnalytics4PropertyRead:
    """Create a new ga4 properties.

    Permissions:
    ------------
    `role=admin|manager` : create new ga4 properties for all clients

    `role=user` : create only ga4 properties that belong to any clients associated
        with the current user

    Returns:
    --------
    `GoAnalytics4PropertyRead` : the newly created ga4 property

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=ga4_in.client_id,
    )
    ga4_repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=permissions.db
    )
    data: Dict = ga4_in.model_dump()
    check_title: str = data.get("title", "")
    check_measurement_id: str = data.get("measurement_id", "")
    check_property_id: str = data.get("property_id", "")
    a_ga4_title: GoAnalytics4Property | None = await ga4_repo.read_by(
        field_name="title",
        field_value=check_title,
    )
    a_ga4_measurement_id: GoAnalytics4Property | None = await ga4_repo.read_by(
        field_name="measurement_id",
        field_value=check_measurement_id,
    )
    a_ga4_property_id: GoAnalytics4Property | None = await ga4_repo.read_by(
        field_name="property_id",
        field_value=check_property_id,
    )
    if (
        a_ga4_measurement_id is not None
        or a_ga4_title is not None
        or a_ga4_property_id is not None
    ):
        raise Ga4PropertyAlreadyExists()
    client_repo: ClientRepository = ClientRepository(session=permissions.db)
    a_client: Client | None = await client_repo.read(entry_id=ga4_in.client_id)
    if a_client is None:
        raise ClientNotExists()
    new_ga4: GoAnalytics4Property = await ga4_repo.create(ga4_in)
    # return role based response
    response_out: GoAnalytics4PropertyRead = permissions.get_resource_response(
        resource=new_ga4,
        responses={
            RoleUser: GoAnalytics4PropertyRead,
        },
    )
    return response_out


@router.get(
    "/{ga4_id}",
    name="ga4_property:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_ga4_property_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4PropertyRead,
)
async def ga4_property_read(
    ga4: GoAnalytics4Property = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_ga4_property_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoAnalytics4PropertyRead:
    """Retrieve a single ga4 property by id.

    Permissions:
    ------------
    `role=admin|manager` : read all ga4 properties

    `role=user` : read only ga4 properties that belong to any clients
        associated with the current user

    Returns:
    --------
    `GoAnalytics4PropertyRead` : the ga4 property matching the ga4_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=ga4.client_id,
    )
    # return role based response
    response_out: GoAnalytics4PropertyRead = permissions.get_resource_response(
        resource=ga4,
        responses={
            RoleUser: GoAnalytics4PropertyRead,
        },
    )
    return response_out


@router.patch(
    "/{ga4_id}",
    name="ga4_property:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_ga4_property_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoAnalytics4PropertyRead,
)
async def ga4_property_update(
    ga4_in: GoAnalytics4PropertyUpdate,
    ga4: GoAnalytics4Property = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_ga4_property_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoAnalytics4PropertyRead:
    """Update a ga4 property by id.

    Permissions:
    ------------
    `role=admin|manager` : update all ga4 properties

    `role=user` : update only ga4 properties that belong to any clients associated
        with the current user

    Returns:
    --------
    `GoAnalytics4PropertyRead` : the updated ga4 property

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=ga4_in,
        schema_privileges={
            RoleUser: GoAnalytics4PropertyUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=ga4.client_id,
    )
    ga4_repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=permissions.db
    )
    if ga4_in.title is not None:
        a_ga4: GoAnalytics4Property | None = await ga4_repo.read_by(
            field_name="title", field_value=ga4_in.title
        )
        if a_ga4:
            raise Ga4PropertyAlreadyExists()
    if ga4_in.client_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=ga4_in.client_id,
        )
        client_repo: ClientRepository = ClientRepository(session=permissions.db)
        a_client: Client | None = await client_repo.read(entry_id=ga4_in.client_id)
        if a_client is None:
            raise ClientNotExists()
    updated_ga4: GoAnalytics4Property | None = await ga4_repo.update(
        entry=ga4, schema=ga4_in
    )
    # return role based response
    response_out: GoAnalytics4PropertyRead = permissions.get_resource_response(
        resource=updated_ga4 if updated_ga4 else ga4,
        responses={
            RoleUser: GoAnalytics4PropertyRead,
        },
    )
    return response_out


@router.delete(
    "/{ga4_id}",
    name="ga4_property:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_ga4_property_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def ga4_property_delete(
    ga4: GoAnalytics4Property = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated], get_ga4_property_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a ga4 property by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any ga4 properties

    `role=user` : delete only ga4 properties that belong to any clients associated
        with the current user

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=ga4.client_id,
    )
    ga4_repo: GoAnalytics4PropertyRepository = GoAnalytics4PropertyRepository(
        session=permissions.db
    )
    await ga4_repo.delete(entry=ga4)
    return None
