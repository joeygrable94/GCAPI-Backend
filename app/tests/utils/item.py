from typing import Optional

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.item import ItemsRepository
from app.db.repositories.user import UsersRepository
from app.db.schemas import ItemCreate, ItemRead
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_item(
    db_session: AsyncSession,
    user_repo: UsersRepository,
    *,
    user_id: Optional[UUID4] = None
) -> ItemRead:
    if user_id is None:
        user = await create_random_user(user_repo)
        user_id = user.id
    title = random_lower_string()
    content = random_lower_string()
    items_repo: ItemsRepository = ItemsRepository(session=db_session)
    item = await items_repo.create(
        ItemCreate(title=title, content=content, user_id=user_id)
    )
    return item
