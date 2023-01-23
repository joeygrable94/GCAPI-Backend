from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.api.exceptions import ClientAlreadyExists, ClientNotExists
from app.db.repositories import ClientsRepository
from app.db.schemas import ClientCreate, ClientRead, ClientUpdate, UserReadAdmin
from app.db.tables import Client
from app.security import Permission, get_current_active_user

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="clients:read_clients",
    response_model=List[ClientRead],
)
async def clients_list(
    db: AsyncSession = Depends(get_async_db),
    page: int = 1,
    current_user: UserReadAdmin = Permission("list", get_current_active_user),
) -> List[ClientRead] | List:
    clients_repo: ClientsRepository = ClientsRepository(session=db)
    clients: List[Client] | List[None] | None = await clients_repo.list(page=page)
    if clients and len(clients):  # pragma: no cover
        return [ClientRead.from_orm(c) for c in clients]
    return []  # pragma: no cover


@router.post(
    "/",
    name="clients:create_client",
    response_model=ClientRead,
)
async def clients_create(
    *,
    db: AsyncSession = Depends(get_async_db),
    client_in: ClientCreate,
    current_user: UserReadAdmin = Permission("create", get_current_active_user),
) -> ClientRead:
    try:
        clients_repo: ClientsRepository = ClientsRepository(session=db)
        data: Dict = client_in.dict()
        check_title: Optional[str] = data.get("title")
        if check_title:
            a_client: Optional[Client] = await clients_repo.read_by(
                field_name="title",
                field_value=check_title,
            )
            if a_client:
                raise ClientAlreadyExists()
        new_client: Client = await clients_repo.create(client_in)
        return ClientRead.from_orm(new_client)
    except ClientAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Client exists"
        )


@router.get(
    "/{id}",
    name="clients:read_client",
    response_model=ClientRead,
)
async def clients_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    current_user: UserReadAdmin = Permission("read", get_current_active_user),
) -> ClientRead:
    try:
        clients_repo: ClientsRepository = ClientsRepository(session=db)
        client: Optional[Client] = await clients_repo.read(entry_id=id)
        if not client:
            raise ClientNotExists()
        return ClientRead.from_orm(client)
    except ClientNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )


@router.patch(
    "/{id}",
    name="clients:update_client",
    response_model=ClientRead,
)
async def clients_update(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    client_in: ClientUpdate,
    current_user: UserReadAdmin = Permission("update", get_current_active_user),
) -> ClientRead:
    try:
        clients_repo: ClientsRepository = ClientsRepository(session=db)
        client: Optional[Client] = await clients_repo.read(entry_id=id)
        if not client:
            raise ClientNotExists()
        data: Dict = client_in.dict()
        check_title: Optional[str] = data.get("title")
        if check_title:
            a_client = await clients_repo.read_by(
                field_name="title", field_value=check_title
            )
            if a_client:
                raise ClientAlreadyExists()
        updated_client: Optional[Client] = await clients_repo.update(
            entry=client, schema=client_in
        )
        if not updated_client:
            raise ClientNotExists()
        return ClientRead.from_orm(updated_client)
    except ClientNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    except ClientAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Client exists"
        )


@router.delete(
    "/{id}",
    name="clients:delete_client",
    response_model=None,
)
async def clients_delete(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    current_user: UserReadAdmin = Permission("delete", get_current_active_user),
) -> None:
    try:
        clients_repo: ClientsRepository = ClientsRepository(session=db)
        client: Optional[Client] = await clients_repo.read(entry_id=id)
        if not client:
            raise ClientNotExists()
        await clients_repo.delete(entry=client)
        return None
    except ClientNotExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
