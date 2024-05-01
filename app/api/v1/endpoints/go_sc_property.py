from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonClientWebsiteQueryParams,
    GetClientWebsiteQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_go_search_console_property_404,
    get_permission_controller,
)
from app.api.exceptions import (
    ClientNotExists,
    GoSearchConsolePropertyAlreadyExists,
    WebsiteNotExists,
)
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
from app.crud import (
    ClientRepository,
    GoSearchConsolePropertyRepository,
    WebsiteRepository,
)
from app.models import Client, GoSearchConsoleProperty, Website
from app.schemas import (
    GoSearchConsolePropertyCreate,
    GoSearchConsolePropertyRead,
    GoSearchConsolePropertyUpdate,
)

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="go_search_console_property:list",
    dependencies=[
        Depends(CommonClientWebsiteQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[GoSearchConsolePropertyRead],
)
async def go_search_console_property_list(
    query: GetClientWebsiteQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[GoSearchConsolePropertyRead]:
    """Retrieve a paginated list of google search console properties.

    Permissions:
    ------------
    `role=admin|manager` : all google search console properties

    `role=user` : only google search console properties that belong to the user

    Returns:
    --------
    `Paginated[GoSearchConsolePropertyRead]` : a paginated list of google search
        console properties, optionally filtered

    """
    # formulate the select statement based on the current user's role
    go_sc_repo: GoSearchConsolePropertyRepository = GoSearchConsolePropertyRepository(
        session=permissions.db
    )
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = go_sc_repo.query_list(
            client_id=query.client_id,
            website_id=query.website_id,
        )
    else:
        select_stmt = go_sc_repo.query_list(
            user_id=permissions.current_user.id,
            client_id=query.client_id,
            website_id=query.website_id,
        )
    response_out: Paginated[GoSearchConsolePropertyRead] = (
        await permissions.get_paginated_resource_response(
            table_name=GoSearchConsoleProperty.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: GoSearchConsolePropertyRead,
                RoleManager: GoSearchConsolePropertyRead,
                RoleClient: GoSearchConsolePropertyRead,
                RoleEmployee: GoSearchConsolePropertyRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="go_search_console_property:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=GoSearchConsolePropertyRead,
)
async def go_search_console_property_create(
    go_sc_in: GoSearchConsolePropertyCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoSearchConsolePropertyRead:
    """Create a new google search console properties.

    Permissions:
    ------------
    `role=admin|manager` : create new google search console properties
        for all clients

    `role=user` : create only google search console properties that belong
        to any clients associated with the current user

    Returns:
    --------
    `GoSearchConsolePropertyRead` : the newly created google search console
        property

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_sc_in.client_id,
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=go_sc_in.website_id,
    )
    go_sc_repo: GoSearchConsolePropertyRepository = GoSearchConsolePropertyRepository(
        session=permissions.db
    )
    a_go_sc_title: GoSearchConsoleProperty | None = await go_sc_repo.read_by(
        field_name="title",
        field_value=go_sc_in.title,
    )
    a_go_sc_client_website: GoSearchConsoleProperty | None = (
        await go_sc_repo.exists_by_two(
            field_name_a="client_id",
            field_value_a=go_sc_in.client_id,
            field_name_b="website_id",
            field_value_b=go_sc_in.website_id,
        )
    )
    if a_go_sc_title is not None or a_go_sc_client_website is not None:
        raise GoSearchConsolePropertyAlreadyExists()
    client_repo: ClientRepository = ClientRepository(session=permissions.db)
    a_client: Client | None = await client_repo.read(entry_id=go_sc_in.client_id)
    if a_client is None:
        raise ClientNotExists()
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    a_website: Website | None = await website_repo.read(entry_id=go_sc_in.website_id)
    if a_website is None:
        raise WebsiteNotExists()
    new_go_sc: GoSearchConsoleProperty = await go_sc_repo.create(go_sc_in)
    # return role based response
    response_out: GoSearchConsolePropertyRead = permissions.get_resource_response(
        resource=new_go_sc,
        responses={
            RoleUser: GoSearchConsolePropertyRead,
        },
    )
    return response_out


@router.get(
    "/{gsc_id}",
    name="go_search_console_property:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
    ],
    response_model=GoSearchConsolePropertyRead,
)
async def go_search_console_property_read(
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated],
        get_go_search_console_property_404,
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoSearchConsolePropertyRead:
    """Retrieve a single google search console property by id.

    Permissions:
    ------------
    `role=admin|manager` : read all google search console properties

    `role=user` : read only google search console properties that belong to
        any clients associated with the current user

    Returns:
    --------
    `GoSearchConsolePropertyRead` : the google search console property matching
        the gsc_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_sc.client_id,
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=go_sc.website_id,
    )
    # return role based response
    response_out: GoSearchConsolePropertyRead = permissions.get_resource_response(
        resource=go_sc,
        responses={
            RoleUser: GoSearchConsolePropertyRead,
        },
    )
    return response_out


@router.patch(
    "/{gsc_id}",
    name="go_search_console_property:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
    ],
    response_model=GoSearchConsolePropertyRead,
)
async def go_search_console_property_update(
    go_sc_in: GoSearchConsolePropertyUpdate,
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated],
        get_go_search_console_property_404,
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> GoSearchConsolePropertyRead:
    """Update a google search console property by id.

    Permissions:
    ------------
    `role=admin|manager` : update all google search console properties

    `role=user` : update only google search console properties that belong to
        any clients associated with the current user

    Returns:
    --------
    `GoSearchConsolePropertyRead` : the updated google search console property

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=go_sc_in,
        schema_privileges={
            RoleUser: GoSearchConsolePropertyUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_sc.client_id,
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=go_sc.website_id,
    )
    go_sc_repo: GoSearchConsolePropertyRepository = GoSearchConsolePropertyRepository(
        session=permissions.db
    )
    if go_sc_in.title is not None:
        a_go_sc: GoSearchConsoleProperty | None = await go_sc_repo.read_by(
            field_name="title",
            field_value=go_sc_in.title,
        )
        if a_go_sc:
            raise GoSearchConsolePropertyAlreadyExists()
    if go_sc_in.client_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=go_sc_in.client_id,
        )
        client_repo: ClientRepository = ClientRepository(session=permissions.db)
        a_client: Client | None = await client_repo.read(entry_id=go_sc_in.client_id)
        if a_client is None:
            raise ClientNotExists()
    if go_sc_in.website_id is not None:
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            website_id=go_sc_in.website_id,
        )
        website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
        a_website: Website | None = await website_repo.read(
            entry_id=go_sc_in.website_id
        )
        if a_website is None:
            raise WebsiteNotExists()
    if go_sc_in.client_id is not None and go_sc_in.website_id is not None:
        b_go_sc: GoSearchConsoleProperty | None = await go_sc_repo.exists_by_two(
            field_name_a="client_id",
            field_value_a=go_sc_in.client_id,
            field_name_b="website_id",
            field_value_b=go_sc_in.website_id,
        )
        if b_go_sc:
            raise GoSearchConsolePropertyAlreadyExists()
    updated_go_sc: GoSearchConsoleProperty | None = await go_sc_repo.update(
        entry=go_sc, schema=go_sc_in
    )
    # return role based response
    response_out: GoSearchConsolePropertyRead = permissions.get_resource_response(
        resource=updated_go_sc if updated_go_sc else go_sc,
        responses={
            RoleUser: GoSearchConsolePropertyRead,
        },
    )
    return response_out


@router.delete(
    "/{gsc_id}",
    name="go_search_console_property:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_go_search_console_property_404),
    ],
    response_model=None,
)
async def go_search_console_property_delete(
    go_sc: GoSearchConsoleProperty = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated],
        get_go_search_console_property_404,
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a google search console property by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any google search console properties

    `role=user` : delete only google search console properties that belong to
        any clients associated with the current user

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=go_sc.client_id,
    )
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=go_sc.website_id,
    )
    go_sc_repo: GoSearchConsolePropertyRepository = GoSearchConsolePropertyRepository(
        session=permissions.db
    )
    await go_sc_repo.delete(entry=go_sc)
    return None
