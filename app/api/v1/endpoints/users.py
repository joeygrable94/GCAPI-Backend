from typing import Any, List

from fastapi import APIRouter, Depends
from fastapi_users_db_sqlalchemy import AsyncSession
from pydantic import UUID4

from app.api.deps import get_async_db
from app.db.repositories.user import UsersRepository
from app.db.schemas import UserRead

users_router = APIRouter()


@users_router.get("/", response_model=List[UserRead], name="users:read_users")
async def users_list(page: int = 1, db: AsyncSession = Depends(get_async_db)) -> Any:
    users_repo: UsersRepository = UsersRepository(session=db)
    users = await users_repo.list(page=page)
    return users
