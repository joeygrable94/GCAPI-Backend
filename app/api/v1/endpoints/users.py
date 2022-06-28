from typing import Any, List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.user_manager import current_active_superuser
from app.db.repositories.user import UsersRepository
from app.db.schemas import UserRead

users_router: APIRouter = APIRouter()


@users_router.get("/", response_model=List[UserRead], name="users:read_users")
async def users_list(
    page: int = 1,
    db: AsyncSession = Depends(get_async_db),
    current_superuser: Any = Depends(current_active_superuser),
) -> Any:
    users_repo: UsersRepository = UsersRepository(session=db)
    users: Union[List[UserRead], List[Any], None] = await users_repo.list(page=page)
    return users
