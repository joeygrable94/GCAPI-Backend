from typing import Any

import pytest

from app.core.security.manager import UserManager
from app.db.schemas import ID, UP, UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_user(
    user_manager: UserManager[UP, ID],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=username, password=password, is_active=True)
    user: Any = await user_manager.create(user_create=user_in)
    print(user)
    assert hasattr(user, "id")
    assert user.email == username
    assert user.is_active
    assert not user.is_verified
    assert not user.is_superuser
    assert not hasattr(user, "password")
    assert hasattr(user, "hashed_password")


async def test_read_user(
    user_manager: UserManager[UP, ID],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: Any = await user_manager.create(user_create=user_in)
    user_2: Any = await user_manager.get(id=user.id)
    assert user_2
    assert user.email == username
    assert user_2.email == username
    assert user.id == user_2.id


async def test_update_user(
    user_manager: UserManager[UP, ID],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user: Any = await user_manager.create(user_create=user_in)
    new_password: str = random_lower_string()
    user_in_update: UserUpdate = UserUpdate(password=new_password, is_superuser=True)
    await user_manager.update(user_update=user_in_update, user=user)
    user_2: Any = await user_manager.get(id=user.id)
    assert user_2
    assert user.email == user_2.email
    hashed_password: str = user_manager.password_helper.hash(password)
    (
        is_verified,
        password_hash,
    ) = user_manager.password_helper.verify_and_update(password, hashed_password)
    assert is_verified is True


async def test_delete_user(
    user_manager: UserManager[UP, ID],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: Any = await user_manager.create(user_create=user_in)
    assert user
    user_deleted: Any = await user_manager.delete(user=user)
    assert user_deleted is None


async def test_check_if_user_is_active(
    user_manager: UserManager[UP, ID],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=username, password=password)
    user: Any = await user_manager.create(user_create=user_in)
    assert user.is_active is True


async def test_check_if_user_is_active_inactive(
    user_manager: UserManager[UP, ID],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=username, password=password, is_active=False)
    user: Any = await user_manager.create(user_create=user_in)
    assert user.is_active is False


async def test_check_if_user_is_superuser(
    user_manager: UserManager[UP, ID],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: Any = await user_manager.create(user_create=user_in)
    assert user.is_superuser is True


async def test_check_if_user_is_superuser_normal_user(
    user_manager: UserManager[UP, ID],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=username, password=password)
    user: Any = await user_manager.create(user_create=user_in)
    assert user.is_superuser is False
