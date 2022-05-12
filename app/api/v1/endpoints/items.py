from typing import Any, List
from pydantic import UUID4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users_db_sqlalchemy import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas import UserRead, Item, ItemCreate, ItemUpdate, ItemInDB
from app.core.user_manager import current_active_user
from app.core import crud
from app.api.deps import get_async_session

items_router = APIRouter()


@items_router.get(
    '/',
    response_model=List[Item],
    name="items:read_items"
)
async def read_items(
    db: AsyncSession = Depends(get_async_session),
    skip: int = 0,
    limit: int = 10,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    if current_user.is_superuser:
        items = await crud.item.get_multi(
            db,
            skip=skip,
            limit=limit
        )
    else:
        items = await crud.item.get_multi_by_user(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
    return items


@items_router.post(
    '/',
    response_model=Item,
    name="items:create_item"
)
async def create_item(
    *,
    db: AsyncSession = Depends(get_async_session),
    item_in: ItemCreate,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    item = await crud.item.create_with_user(
        db=db,
        obj_in=item_in,
        user_id=current_user.id
    )
    return item


@items_router.patch(
    '/{id}',
    response_model=Item,
    name="items:update_item"
)
async def update_item(
    *,
    db: AsyncSession = Depends(get_async_session),
    id: UUID4,
    item_in: ItemUpdate,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    item = await crud.item.get(
        db=db,
        id=id
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found'
        )
    if not current_user.is_superuser and (item.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions'
        )
    item = await crud.item.update(
        db=db,
        db_obj=item,
        obj_in=item_in
    )
    return item


@items_router.get(
    '/{id}',
    response_model=Item,
    name="items:read_item"
)
async def read_item(
    *,
    db: AsyncSession = Depends(get_async_session),
    id: UUID4,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    item = await crud.item.get(
        db=db,
        id=id
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found'
        )
    if not current_user.is_superuser and (item.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions'
        )
    return item


@items_router.delete(
    '/{id}',
    response_model=Item,
    name="items:delete_item"
)
async def delete_item(
    *,
    db: AsyncSession = Depends(get_async_session),
    id: UUID4,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    item = await crud.item.get(
        db=db,
        id=id
    )
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found'
        )
    if not current_user.is_superuser and (item.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions'
        )
    item = await crud.item.remove(
        db=db,
        id=id
    )
    return item

