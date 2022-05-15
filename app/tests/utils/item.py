from typing import Optional

from sqlalchemy.orm import Session

from app.core import crud
from app.core.models import Item
from app.core.schemas.item import ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


async def create_random_item(
    db: Session,
    *,
    user_id: Optional[int] = None
    ) -> Item:
    if user_id is None:
        user = await create_random_user(db)
        user_id = user.id
    title = random_lower_string()
    content = random_lower_string()
    item_in = ItemCreate(title=title, content=content)
    return await crud.item.create_with_user(db=db, obj_in=item_in, user_id=user_id)
