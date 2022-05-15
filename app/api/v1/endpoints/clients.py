from typing import Any, List
from pydantic import UUID4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import UserRead, Client, ClientCreate, ClientUpdate
from app.core.user_manager import current_active_user, current_active_super_user
from app.core import crud
from app.api.deps import get_async_session

clients_router = APIRouter()


@clients_router.get(
    '/',
    response_model=List[Client],
    name="clients:read_clients"
)
async def read_clients(
    db: AsyncSession = Depends(get_async_session),
    skip: int = 0,
    limit: int = 10,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    # if current_user.is_superuser:
    clients = await crud.client.get_multi(
        db,
        skip=skip,
        limit=limit
    )
    # else:
    #     clients = await crud.client.get_multi_by_user(
    #         db=db,
    #         user_id=current_user.id,
    #         skip=skip,
    #         limit=limit
    #     )
    return clients


@clients_router.post(
    '/',
    response_model=Client,
    name="clients:create_client"
)
async def create_client(
    *,
    db: AsyncSession = Depends(get_async_session),
    client_in: ClientCreate,
    current_user: UserRead = Depends(current_active_super_user),
) -> Any:
    client = await crud.client.create(
        db=db,
        obj_in=client_in,
    )
    return client


@clients_router.patch(
    '/{id}',
    response_model=Client,
    name="clients:update_client"
)
async def update_client(
    *,
    db: AsyncSession = Depends(get_async_session),
    id: UUID4,
    client_in: ClientUpdate,
    current_user: UserRead = Depends(current_active_super_user),
) -> Any:
    client = await crud.client.get(
        db=db,
        id=id
    )
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Client not found'
        )
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions'
        )
    client = await crud.client.update(
        db=db,
        db_obj=client,
        obj_in=client_in
    )
    return client


@clients_router.get(
    '/{id}',
    response_model=Client,
    name="clients:read_client"
)
async def read_client(
    *,
    db: AsyncSession = Depends(get_async_session),
    id: UUID4,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    client = await crud.client.get(
        db=db,
        id=id
    )
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Client not found'
        )
    return client


@clients_router.delete(
    '/{id}',
    response_model=Client,
    name="clients:delete_client"
)
async def delete_client(
    *,
    db: AsyncSession = Depends(get_async_session),
    id: UUID4,
    current_user: UserRead = Depends(current_active_super_user),
) -> Any:
    client = await crud.client.get(
        db=db,
        id=id
    )
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Client not found'
        )
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions'
        )
    client = await crud.client.remove(
        db=db,
        id=id
    )
    return client

