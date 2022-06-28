from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.item import ItemsRepository
from app.db.repositories.user import UsersRepository
from app.db.schemas import ItemCreate
from app.db.schemas.item import ItemRead, ItemUpdate
from app.db.schemas.user import UserRead
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_item(db_session: AsyncSession) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    item_repo: ItemsRepository = ItemsRepository(session=db_session)
    item: ItemRead = await item_repo.create(
        ItemCreate(title=title, content=content, user_id=None)
    )
    assert item.title == title
    assert item.content == content
    assert item.user_id is None


async def test_create_item_with_user(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    title: str = random_lower_string()
    content: str = random_lower_string()
    user: UserRead = await create_random_user(user_repo)
    item_repo: ItemsRepository = ItemsRepository(session=db_session)
    item: ItemRead = await item_repo.create(
        ItemCreate(title=title, content=content, user_id=user.id)
    )
    assert item.title == title
    assert item.content == content
    assert item.user_id == user.id


async def test_get_item(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    title: str = random_lower_string()
    content: str = random_lower_string()
    user: UserRead = await create_random_user(user_repo)
    item_repo: ItemsRepository = ItemsRepository(session=db_session)
    item: ItemRead = await item_repo.create(
        ItemCreate(title=title, content=content, user_id=user.id)
    )
    stored_item: ItemRead = await item_repo.read(entry_id=item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.title == stored_item.title
    assert item.content == stored_item.content
    assert item.user_id == stored_item.user_id


async def test_update_item(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    title: str = random_lower_string()
    content: str = random_lower_string()
    user: UserRead = await create_random_user(user_repo)
    item_repo: ItemsRepository = ItemsRepository(session=db_session)
    item: ItemRead = await item_repo.create(
        ItemCreate(title=title, content=content, user_id=user.id)
    )
    content2: str = random_lower_string()
    item2: ItemRead = await item_repo.update(
        entry_id=item.id, schema=ItemUpdate(content=content2)
    )
    assert item.id == item2.id
    assert item.title == item2.title
    assert item2.content == content2
    assert item.user_id == item2.user_id


async def test_delete_item(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    title: str = random_lower_string()
    content: str = random_lower_string()
    user: UserRead = await create_random_user(user_repo)
    item_repo: ItemsRepository = ItemsRepository(session=db_session)
    item: ItemRead = await item_repo.create(
        ItemCreate(title=title, content=content, user_id=user.id)
    )
    item2: Any = await item_repo.delete(entry_id=item.id)
    item3: Any = await item_repo.read(entry_id=item.id)
    assert item2.id == item.id
    assert item2.title == title
    assert item2.content == content
    assert item2.user_id == user.id
    assert item3 is None
