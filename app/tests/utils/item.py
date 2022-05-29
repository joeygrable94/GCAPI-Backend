from typing import Optional
import fastapi_users

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.item import ItemsRepository
from app.db.schemas import ItemRead, ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_item(
    db_session: AsyncSession,
    user_manager: fastapi_users.BaseUserManager,
    *,
    user_id: Optional[int] = None
) -> ItemRead:
    if user_id is None:
        user = await create_random_user(user_manager)
        user_id = user.id
    title = random_lower_string()
    content = random_lower_string()
    items_repo: ItemsRepository = ItemsRepository(session=db_session)
    item = await items_repo.create(
        ItemCreate(title=title, content=content),
        uid=user_id
    )
    return item
