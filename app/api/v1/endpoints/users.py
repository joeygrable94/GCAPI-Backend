from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_users_db_sqlalchemy import AsyncSession, SQLAlchemyUserDatabase
from sqlalchemy import select

from app.api.deps import get_user_db
from app.core.user_manager import UserManager, current_active_super_user, get_user_manager
from app.db.schemas import UserRead

users_router = APIRouter()


@users_router.get("/", response_model=List[UserRead], name="users:read_users")
async def users_list(
    skip: int = 0,
    limit: int = 10,
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
    current_super_user: UserRead = Depends(current_active_super_user),
) -> Any:
    try:
        statement = select(user_db.user_table).limit(limit).offset(skip)
        result = await user_db.session.execute(statement)
        data = result.scalars().all()
        return data
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
