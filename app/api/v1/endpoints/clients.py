from typing import Dict

from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchClientOr404,
    PermissionController,
    get_async_db,
    get_client_or_404,
    get_current_user,
    get_permission_controller,
)
from app.api.exceptions import ClientAlreadyExists
from app.api.openapi import clients_read_responses
from app.core.pagination import GetPaginatedQueryParams, PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
)
from app.crud import ClientRepository
from app.models import Client
from app.schemas import ClientCreate, ClientRead, ClientUpdate

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="clients:list",
    dependencies=[
        Depends(PageParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[ClientRead],
)
async def clients_list(
    query: GetPaginatedQueryParams,
    db: AsyncDatabaseSession,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[ClientRead]:
    """Retrieve a paginated list of clients.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    `role=client|employee` : only clients associated with the user via `user_client`
        table

    Returns:
    --------
    `List[ClientRead] | List[None]` : a list of clients, optionally filtered,
        or returns an empty list

    """
    clients_repo: ClientRepository = ClientRepository(session=db)
    response_out: Paginated[
        ClientRead
    ] = await permissions.get_paginated_resource_response(
        table_name=Client.__tablename__,
        stmt=clients_repo.query_list(),
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
    ],
    response_model=ClientRead,
)
async def clients_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    client_in: ClientCreate,
) -> ClientRead:
    """Create a new client.

    Permissions:
    ------------
    `role=admin|manager` : create a new client

    Returns:
    --------
    `ClientRead` : the newly created client

    """
    clients_repo: ClientRepository = ClientRepository(session=db)
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
    return ClientRead.model_validate(new_client)


@router.get(
    "/{client_id}",
    name="clients:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
    ],
    responses=clients_read_responses,
    response_model=ClientRead,
)
async def clients_read(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    client: FetchClientOr404,
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
    return ClientRead.model_validate(client)


@router.patch(
    "/{client_id}",
    name="clients:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
    ],
    response_model=ClientRead,
)
async def clients_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    client: FetchClientOr404,
    client_in: ClientUpdate,
) -> ClientRead:
    """Update a client by id.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    Returns:
    --------
    `ClientRead` : the updated client

    """
    clients_repo: ClientRepository = ClientRepository(session=db)
    if client_in.title is not None:
        a_client: Client | None = await clients_repo.read_by(
            field_name="title", field_value=client_in.title
        )
        if a_client:
            raise ClientAlreadyExists()
    updated_client: Client | None = await clients_repo.update(
        entry=client, schema=client_in
    )
    return (
        ClientRead.model_validate(updated_client)
        if updated_client
        else ClientRead.model_validate(client)
    )


@router.delete(
    "/{client_id}",
    name="clients:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
    ],
    response_model=None,
)
async def clients_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    client: FetchClientOr404,
) -> None:
    """Delete a client by id.

    Permissions:
    ------------
    `role=admin` : all clients

    Returns:
    --------
    `None`

    """
    clients_repo: ClientRepository = ClientRepository(session=db)
    await clients_repo.delete(entry=client)
    return None
