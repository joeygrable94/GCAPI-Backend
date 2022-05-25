from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.user_manager import current_active_super_user
from app.db.schemas import UserRead
from app.api.deps import get_user_db


users_router = APIRouter()


@users_router.get(
    "/",
    response_model=List[UserRead],
    name="users:read_users"
)
async def read_users(
    user_db: AsyncSession = Depends(get_user_db),
    skip: int = 0,
    limit: int = 10,
    current_super_user: UserRead = Depends(current_active_super_user),
):
    try:
        statement = select(user_db.user_table).limit(limit).offset(skip)
        result = await user_db.session.execute(statement)
        return result.scalars().all()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

