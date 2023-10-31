from typing import Dict, List

from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchClientOr404,
    get_async_db,
    get_client_or_404,
)
from app.api.exceptions import ClientAlreadyExists
from app.api.openapi import clients_read_responses
from app.core.pagination import GetPaginatedQueryParams
from app.core.security import auth
from app.crud import ClientRepository
from app.models import Client
from app.schemas import ClientCreate, ClientRead, ClientUpdate

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="clients:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[ClientRead],
)
async def clients_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetPaginatedQueryParams,
) -> List[ClientRead] | List:
    """Retrieve a list of clients.

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
    clients: List[Client] | List[None] | None = await clients_repo.list(page=query.page)
    return [ClientRead.model_validate(c) for c in clients] if clients else []


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
