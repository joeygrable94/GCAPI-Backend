from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.security import get_current_active_user
from app.db.repositories.client import ClientsRepository
from app.db.schemas import ClientCreate, ClientRead, ClientUpdate, UserRead

clients_router: APIRouter = APIRouter()


@clients_router.get("/", response_model=List[ClientRead], name="clients:read_clients")
async def clients_list(
    db: AsyncSession = Depends(get_async_db),
    page: int = 1,
    current_user: UserRead = Depends(get_current_active_user),
) -> Union[List[ClientRead], List[Any], None]:
    clients_repo: ClientsRepository = ClientsRepository(session=db)
    clients = await clients_repo.list(page=page)
    if clients:
        return clients
    return list()


@clients_router.post("/", response_model=ClientRead, name="clients:create_client")
async def clients_create(
    *,
    db: AsyncSession = Depends(get_async_db),
    client_in: ClientCreate,
    current_user: UserRead = Depends(get_current_active_user),
) -> ClientRead:
    clients_repo: ClientsRepository = ClientsRepository(session=db)
    client: ClientRead = await clients_repo.create(client_in)
    return client


@clients_router.get("/{id}", response_model=ClientRead, name="clients:read_client")
async def clients_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    current_user: UserRead = Depends(get_current_active_user),
) -> ClientRead:
    clients_repo: ClientsRepository = ClientsRepository(session=db)
    client: Optional[ClientRead] = await clients_repo.read(entry_id=id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return client


@clients_router.patch("/{id}", response_model=ClientRead, name="clients:update_client")
async def clients_update(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    client_in: ClientUpdate,
    current_user: UserRead = Depends(get_current_active_user),
) -> Any:
    clients_repo: ClientsRepository = ClientsRepository(session=db)
    client: Optional[ClientRead] = await clients_repo.read(entry_id=id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    client = await clients_repo.update(entry_id=id, schema=client_in)
    return client


@clients_router.delete("/{id}", response_model=ClientRead, name="clients:delete_client")
async def clients_delete(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    current_user: UserRead = Depends(get_current_active_user),
) -> Any:
    clients_repo: ClientsRepository = ClientsRepository(session=db)
    client: Optional[ClientRead] = await clients_repo.read(entry_id=id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    client = await clients_repo.delete(entry_id=id)
    return client
