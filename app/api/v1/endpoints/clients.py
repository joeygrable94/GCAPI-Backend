from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonUserQueryParams,
    GetUserQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_client_or_404,
    get_current_user,
    get_permission_controller,
)
from app.api.exceptions import (
    ClientAlreadyExists,
    ClientNotExists,
    UserNotExists,
    WebsiteNotExists,
)
from app.api.openapi import clients_read_responses
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
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
    ClientWebsiteRepository,
    UserClientRepository,
    UserRepository,
    WebsiteRepository,
)
from app.models import Client, ClientWebsite, User, UserClient, Website
from app.schemas import (
    ClientCreate,
    ClientDelete,
    ClientRead,
    ClientUpdate,
    ClientWebsiteCreate,
    UserClientCreate,
)
from app.worker import task_request_to_delete_client

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="clients:list",
    dependencies=[
        Depends(CommonUserQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[ClientRead],
)
async def clients_list(
    query: GetUserQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[ClientRead]:
    """Retrieve a paginated list of clients.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    `role=user` : only clients associated with the user via `user_client`
        table

    Returns:
    --------
    `Paginated[ClientRead]` : a paginated list of clients, optionally filtered

    """
    # formulate the select statement based on the current user's role
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = permissions.client_repo.query_list(user_id=query.user_id)
    else:  # TODO: test
        select_stmt = permissions.client_repo.query_list(
            user_id=permissions.current_user.id
        )
    # return role based response
    response_out: Paginated[
        ClientRead
    ] = await permissions.get_paginated_resource_response(
        table_name=Client.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleAdmin: ClientRead,
            RoleManager: ClientRead,
            RoleClient: ClientRead,
            RoleEmployee: ClientRead,
        },
    )
    return response_out


@router.post(
    "/",
    name="clients:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_create(
    client_in: ClientCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Create a new client.

    Permissions:
    ------------
    `role=admin|manager` : create a new client

    Returns:
    --------
    `ClientRead` : the newly created client

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    clients_repo: ClientRepository = ClientRepository(session=permissions.db)
    data: Dict = client_in.model_dump()
    check_title: str | None = data.get("title")
    if check_title:
        a_client: Client | None = await clients_repo.read_by(
            field_name="title",
            field_value=check_title,
        )
        if a_client:
            raise ClientAlreadyExists()
    new_client: Client = await clients_repo.create(client_in)
    # return role based response
    response_out: ClientRead = permissions.get_resource_response(
        resource=new_client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


@router.get(
    "/{client_id}",
    name="clients:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    responses=clients_read_responses,
    response_model=ClientRead,
)
async def clients_read(
    client: Client = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_client_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Retrieve a single client by id.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    `role=user` : only clients associated with the user via `user_client`

    Returns:
    --------
    `ClientRead` : a client matching the client_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    # return role based response
    response_out: ClientRead = permissions.get_resource_response(
        resource=client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


@router.patch(
    "/{client_id}",
    name="clients:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_update(
    client_in: ClientUpdate,
    client: Client = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_client_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Update a client by id.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    `role=user` : only clients associated with the user via `user_client`

    Returns:
    --------
    `ClientRead` : the updated client

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=client_in,
        schema_privileges={
            RoleUser: ClientUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    clients_repo: ClientRepository = ClientRepository(session=permissions.db)
    if client_in.title is not None:
        a_client: Client | None = await clients_repo.read_by(
            field_name="title", field_value=client_in.title
        )
        if a_client:
            raise ClientAlreadyExists()
    updated_client: Client | None = await clients_repo.update(
        entry=client, schema=client_in
    )
    # return role based response
    response_out: ClientRead = permissions.get_resource_response(
        resource=updated_client if updated_client else client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


@router.delete(
    "/{client_id}",
    name="clients:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientDelete,
)
async def clients_delete(
    client: Client = Permission([AccessDelete, AccessDeleteSelf], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientDelete:
    """Delete a client by id.

    Permissions:
    ------------
    `role=admin` : all clients

    `role=client` : may request to have their client data deleted

    Returns:
    --------
    `ClientDelete` : a message indicating the user deleted a client or if a user
        requested to delete a client they are associated with

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin], client_id=client.id
    )
    client_delete: ClientDelete
    if RoleAdmin in permissions.privileges:
        clients_repo: ClientRepository = ClientRepository(session=permissions.db)
        await clients_repo.delete(entry=client)
        client_delete = ClientDelete(
            message="Client deleted",
            user_id=permissions.current_user.id,
            client_id=client.id,
        )
    else:  # TODO: test
        delete_client_task: Any = task_request_to_delete_client.delay(
            user_id=permissions.current_user.id, client_id=client.id
        )
        client_delete = ClientDelete(
            message="Client requested to be deleted",
            user_id=permissions.current_user.id,
            client_id=client.id,
            task_id=delete_client_task.task_id,
        )
    return client_delete


# client relationships


@router.post(
    "/{client_id}/user",
    name="clients:assign_user",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_assign_user(
    user_client_in: UserClientCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Assigns a user to a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `ClientRead` : the updated client

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=user_client_in,
        schema_privileges={
            RoleAdmin: UserClientCreate,
            RoleManager: UserClientCreate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    # check if client and user exists
    if user_client_in.client_id != client.id:
        raise ClientNotExists()
    user_repo: UserRepository = UserRepository(session=permissions.db)
    user_exists: User | None = await user_repo.read(entry_id=user_client_in.user_id)
    if user_exists is None:
        raise UserNotExists()
    user_client_repo: UserClientRepository = UserClientRepository(
        session=permissions.db
    )
    user_client_exists: UserClient | None = await user_client_repo.exists_by_two(
        "user_id", user_client_in.user_id, "client_id", user_client_in.client_id
    )
    if user_client_exists is None:
        user_client_exists = await user_client_repo.create(schema=user_client_in)
    client_repo: ClientRepository = ClientRepository(session=permissions.db)
    client_out: Client | None = await client_repo.read(user_client_exists.client_id)
    # return role based response
    response_out: ClientRead = permissions.get_resource_response(
        resource=client_out if client_out else client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


@router.delete(
    "/{client_id}/user",
    name="clients:remove_user",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_remove_user(
    user_client_in: UserClientCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Removes a user from a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `ClientRead` : the updated client

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=user_client_in,
        schema_privileges={
            RoleAdmin: UserClientCreate,
            RoleManager: UserClientCreate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    # check if client and user exists
    if user_client_in.client_id != client.id:
        raise ClientNotExists()
    user_repo: UserRepository = UserRepository(session=permissions.db)
    user_exists: User | None = await user_repo.read(entry_id=user_client_in.user_id)
    if user_exists is None:
        raise UserNotExists()
    user_client_repo: UserClientRepository = UserClientRepository(
        session=permissions.db
    )
    user_client_exists: UserClient | None = await user_client_repo.exists_by_two(
        "user_id", user_client_in.user_id, "client_id", user_client_in.client_id
    )
    if user_client_exists is not None:
        await user_client_repo.delete(user_client_exists)
    # return role based response
    response_out: ClientRead = permissions.get_resource_response(
        resource=client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


@router.post(
    "/{client_id}/website",
    name="clients:assign_website",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_assign_website(
    client_website_in: ClientWebsiteCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Assigns a website to a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `ClientRead` : the updated client

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=client_website_in,
        schema_privileges={
            RoleAdmin: ClientWebsiteCreate,
            RoleManager: ClientWebsiteCreate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], website_id=client_website_in.website_id
    )
    # check if client and user exists
    if client_website_in.client_id != client.id:
        raise ClientNotExists()
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    website_exists: Website | None = await website_repo.read(
        entry_id=client_website_in.website_id
    )
    if website_exists is None:
        raise WebsiteNotExists()
    client_website_repo: ClientWebsiteRepository = ClientWebsiteRepository(
        session=permissions.db
    )
    client_website_exists: ClientWebsite | None = (
        await client_website_repo.exists_by_two(
            "website_id",
            client_website_in.website_id,
            "client_id",
            client_website_in.client_id,
        )
    )
    if client_website_exists is None:
        client_website_exists = await client_website_repo.create(
            schema=client_website_in
        )
    client_repo: ClientRepository = ClientRepository(session=permissions.db)
    client_out: Client | None = await client_repo.read(client_website_exists.client_id)
    # return role based response
    response_out: ClientRead = permissions.get_resource_response(
        resource=client_out if client_out else client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


@router.delete(
    "/{client_id}/website",
    name="clients:remove_website",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_remove_website(
    client_website_in: ClientWebsiteCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Removes a website from a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `ClientRead` : the updated client

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=client_website_in,
        schema_privileges={
            RoleAdmin: ClientWebsiteCreate,
            RoleManager: ClientWebsiteCreate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], website_id=client_website_in.website_id
    )
    # check if client and user exists
    if client_website_in.client_id != client.id:
        raise ClientNotExists()
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    website_exists: Website | None = await website_repo.read(
        entry_id=client_website_in.website_id
    )
    if website_exists is None:
        raise WebsiteNotExists()
    client_website_repo: ClientWebsiteRepository = ClientWebsiteRepository(
        session=permissions.db
    )
    client_website_exists: ClientWebsite | None = (
        await client_website_repo.exists_by_two(
            "website_id",
            client_website_in.website_id,
            "client_id",
            client_website_in.client_id,
        )
    )
    if client_website_exists is not None:
        await client_website_repo.delete(client_website_exists)
    # return role based response
    response_out: ClientRead = permissions.get_resource_response(
        resource=client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out
