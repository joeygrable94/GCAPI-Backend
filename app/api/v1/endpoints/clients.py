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
from app.api.exceptions import ClientAlreadyExists
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
from app.crud import ClientRepository
from app.models import Client
from app.schemas import ClientCreate, ClientDelete, ClientRead, ClientUpdate
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
