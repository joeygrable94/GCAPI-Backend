from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_users import BaseUserManager
from sqlalchemy import select
from app.core.user_manager import current_active_super_user, get_user_manager
from app.db.schemas import UserRead


users_router = APIRouter()


@users_router.get(
    "/",
    response_model=List[UserRead],
    name="users:read_users"
)
async def read_users(
    user_manager: BaseUserManager = Depends(get_user_manager),
    skip: int = 0,
    limit: int = 10,
    current_super_user: UserRead = Depends(current_active_super_user),
):
    try:
        statement = select(user_manager.user_db.user_table).limit(limit).offset(skip)
        result = await user_manager.user_db.session.execute(statement)
        return result.scalars().all()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

