from typing import Any

import pytest
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user import UsersRepository
from app.db.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_user(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: EmailStr = random_email()
    password: str = random_lower_string()
    user: Any = await user_repo.create(
        schema=UserCreate(email=username, password=password)
    )
    assert hasattr(user, "id")
    assert user.email == username
    assert user.is_active
    assert not hasattr(user, "password")
    assert not hasattr(user, "hashed_password")
    assert not user.is_verified
    assert not user.is_superuser


async def test_read_user(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: EmailStr = random_email()
    password: str = random_lower_string()
    user: Any = await user_repo.create(
        UserCreate(email=username, password=password, is_superuser=True)
    )
    user_2: Any = await user_repo.read(user_id=user.id)
    assert user_2
    assert user.email == username
    assert user_2.email == username
    assert user.id == user_2.id


async def test_update_user(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: EmailStr = random_email()
    password: str = random_lower_string()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user: Any = await user_repo.create(schema=user_in)
    new_password: str = random_lower_string()
    user_in_update: UserUpdate = UserUpdate(password=new_password, is_superuser=True)
    await user_repo.update(user_id=user.id, schema=user_in_update)
    user_2: Any = await user_repo.read(user_id=user.id)
    assert user_2
    assert user.email == user_2.email
    hashed_password: str = user_repo._user_manager.password_helper.hash(password)
    (
        is_verified,
        password_hash,
    ) = user_repo._user_manager.password_helper.verify_and_update(
        password, hashed_password
    )
    assert is_verified is True


async def test_delete_user(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: EmailStr = random_email()
    password: str = random_lower_string()
    user: Any = await user_repo.create(
        schema=UserCreate(email=username, password=password, is_superuser=True)
    )
    assert user
    user_deleted: Any = await user_repo.delete(user_id=user.id)
    assert user_deleted == user


async def test_check_if_user_is_active(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: EmailStr = random_email()
    password: str = random_lower_string()
    user: Any = await user_repo.create(
        schema=UserCreate(email=username, password=password)
    )
    assert user.is_active is True


async def test_check_if_user_is_active_inactive(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: EmailStr = random_email()
    password: str = random_lower_string()
    user: Any = await user_repo.create(
        schema=UserCreate(email=username, password=password, is_active=False)
    )
    assert user.is_active is False


async def test_check_if_user_is_superuser(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: EmailStr = random_email()
    password: str = random_lower_string()
    user: Any = await user_repo.create(
        UserCreate(email=username, password=password, is_superuser=True)
    )
    assert user.is_superuser is True


async def test_check_if_user_is_superuser_normal_user(
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    username: EmailStr = random_email()
    password: str = random_lower_string()
    user: Any = await user_repo.create(
        schema=UserCreate(email=username, password=password)
    )
    assert user.is_superuser is False
