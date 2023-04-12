from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchClientOr404,
    GetClientWebsiteQueryParams,
    get_async_db,
    get_client_or_404,
)
from app.api.errors import ErrorCode
from app.api.exceptions import ClientAlreadyExists
from app.core.auth import auth
from app.crud import ClientRepository
from app.models import Client
from app.schemas import ClientCreate, ClientRead, ClientReadRelations, ClientUpdate

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="clients:list",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=List[ClientReadRelations],
)
async def clients_list(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    query: GetClientWebsiteQueryParams,
) -> List[ClientRead] | List:
    clients_repo: ClientRepository = ClientRepository(session=db)
    clients: List[Client] | List[None] | None = await clients_repo.list(page=query.page)
    return [ClientRead.from_orm(c) for c in clients] if len(clients) else []


@router.post(
    "/",
    name="clients:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=ClientReadRelations,
)
async def clients_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    client_in: ClientCreate,
) -> ClientRead:
    try:
        clients_repo: ClientRepository = ClientRepository(session=db)
        data: Dict = client_in.dict()
        check_title: str | None = data.get("title")
        if check_title:
            a_client: Client | None = await clients_repo.read_by(
                field_name="title",
                field_value=check_title,
            )
            if a_client:
                raise ClientAlreadyExists()
        new_client: Client = await clients_repo.create(client_in)
        return ClientRead.from_orm(new_client)
    except ClientAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.CLIENT_EXISTS
        )


@router.get(
    "/{client_id}",
    name="clients:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
    ],
    response_model=ClientReadRelations,
)
async def clients_read(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    client: FetchClientOr404,
) -> ClientRead:
    return ClientRead.from_orm(client)


@router.patch(
    "/{client_id}",
    name="clients:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
    ],
    response_model=ClientReadRelations,
)
async def clients_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    client: FetchClientOr404,
    client_in: ClientUpdate,
) -> ClientRead:
    try:
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
        return ClientRead.from_orm(updated_client) if updated_client else ClientRead.from_orm(client)
    except ClientAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.CLIENT_EXISTS
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
    clients_repo: ClientRepository = ClientRepository(session=db)
    await clients_repo.delete(entry=client)
    return None
