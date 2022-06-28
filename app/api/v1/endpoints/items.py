from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.user_manager import current_active_user
from app.db.repositories.item import ItemsRepository
from app.db.schemas import ItemCreate, ItemRead, ItemUpdate, UserRead

items_router: APIRouter = APIRouter()


@items_router.get("/", response_model=List[ItemRead], name="items:read_items")
async def items_list(
    db: AsyncSession = Depends(get_async_db),
    page: int = 1,
    user_id: UUID4 = None,
    current_user: UserRead = Depends(current_active_user),
) -> List[ItemRead]:
    items_repo: ItemsRepository = ItemsRepository(session=db)
    items: List[ItemRead] = await items_repo.list(page=page, user_id=user_id)
    return items


@items_router.post("/", response_model=ItemRead, name="items:create_item")
async def items_create(
    *,
    db: AsyncSession = Depends(get_async_db),
    item_in: ItemCreate,
    current_user: UserRead = Depends(current_active_user),
) -> ItemRead:
    items_repo: ItemsRepository = ItemsRepository(session=db)
    if not item_in.user_id:
        item_in.user_id = current_user.id
    item: ItemRead = await items_repo.create(item_in)
    return item


@items_router.get("/{id}", response_model=ItemRead, name="items:read_item")
async def items_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    current_user: UserRead = Depends(current_active_user),
) -> ItemRead:
    items_repo: ItemsRepository = ItemsRepository(session=db)
    item: ItemRead = await items_repo.read(entry_id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    if current_user.is_superuser or current_user.id == item.user_id:
        return item
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
    )


@items_router.patch("/{id}", response_model=ItemRead, name="items:update_item")
async def items_update(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    item_in: ItemUpdate,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    items_repo: ItemsRepository = ItemsRepository(session=db)
    item: ItemRead = await items_repo.read(entry_id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    if current_user.is_superuser or current_user.id == item.user_id:
        item = await items_repo.update(entry_id=id, schema=item_in)
        return item
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
    )


@items_router.delete("/{id}", response_model=ItemRead, name="items:delete_item")
async def items_delete(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    current_user: UserRead = Depends(current_active_user),
) -> Any:
    items_repo: ItemsRepository = ItemsRepository(session=db)
    item: ItemRead = await items_repo.read(entry_id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    if current_user.is_superuser or current_user.id == item.user_id:
        item = await items_repo.delete(entry_id=id)
        return item
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions"
    )
