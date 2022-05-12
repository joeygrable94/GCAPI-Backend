from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud.base import CRUDBase
from app.core.models.item import Item
from app.core.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):

    async def create_with_user(
        self,
        db: AsyncSession,
        *,
        obj_in: ItemCreate,
        user_id: int
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[Item]:
        statement = select(self.model)\
            .where(Item.user_id == user_id)\
            .offset(skip)\
            .limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()


item = CRUDItem(Item)
