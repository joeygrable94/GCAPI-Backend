from typing import Any, Optional

import pytest
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_email, random_lower_string

from app.api.exceptions import (
    ApiAuthException,
    InvalidPasswordException,
    UserAlreadyExists,
)
from app.core.config import settings
from app.core.utilities import password_helper
from app.db.repositories import UserRepository
from app.db.schemas import UserCreate, UserUpdate
from app.db.schemas.user import UserUpdateAuthPermissions
from app.db.tables import User

pytestmark = pytest.mark.asyncio


async def test_user_repo_table(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    assert user_repo._table is User


async def test_create_user(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=username, password=password, is_active=True)
    user: User = await user_repo.create(schema=user_in)
    assert hasattr(user, "id")
    assert user.email == username
    assert user.is_active
    assert not user.is_verified
    assert not user.is_superuser
    assert not hasattr(user, "password")
    assert hasattr(user, "hashed_password")


async def test_create_user_password_too_short(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = "abc123"
    user_in: UserCreate = UserCreate(email=username, password=password, is_active=True)
    with pytest.raises(InvalidPasswordException):
        user: User = await user_repo.create(schema=user_in)  # noqa: F841


async def test_create_user_password_too_long(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string() * 4
    user_in: UserCreate = UserCreate(email=username, password=password, is_active=True)
    with pytest.raises(InvalidPasswordException):
        user: User = await user_repo.create(schema=user_in)  # noqa: F841


async def test_create_user_already_exists(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=username, password=password, is_active=True)
    user: User = await user_repo.create(schema=user_in)
    assert user
    with pytest.raises(UserAlreadyExists):
        user_2: User = await user_repo.create(schema=user_in)  # noqa: F841


async def test_read_user(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: User = await user_repo.create(schema=user_in)
    user_2: Optional[User] = await user_repo.read(entry_id=user.id)
    assert user is user_2
    assert user.email == username
    assert user_2.email == username
    assert user.id == user_2.id


async def test_update_user(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: User = await user_repo.create(schema=user_in)
    new_password: str = random_lower_string()
    user_in_update: UserUpdate = UserUpdate(password=new_password, is_superuser=True)
    await user_repo.update(entry=user, schema=user_in_update)
    user_2: Optional[User] = await user_repo.read(entry_id=user.id)
    assert user_2
    assert user.email == user_2.email
    hashed_password: str = password_helper.hash(password)
    (
        is_verified,
        password_hash,  # noqa: F841
    ) = password_helper.verify_and_update(password, hashed_password)
    assert is_verified is True


async def test_delete_user(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: User = await user_repo.create(schema=user_in)
    assert user
    user_deleted: Any = await user_repo.delete(entry=user)  # type: ignore
    assert user_deleted is None


async def test_authenticate_user(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    login_form: OAuth2PasswordRequestForm = OAuth2PasswordRequestForm(
        grant_type="password",
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        scope="",
    )
    user: Optional[User] = await user_repo.authenticate(credentials=login_form)
    assert user
    assert user.id
    assert user.email == settings.FIRST_SUPERUSER
    assert user.hashed_password
    assert user.is_active
    assert user.is_verified
    assert user.is_superuser


async def test_authenticate_user_raise_not_exists(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    login_form: OAuth2PasswordRequestForm = OAuth2PasswordRequestForm(
        grant_type="password",
        username=random_email(),
        password=random_lower_string(),
        scope="",
    )
    user: Optional[User] = await user_repo.authenticate(credentials=login_form)
    assert user is None


async def test_crud_update_permissions_add(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: User = await user_repo.create(schema=user_in)
    assert user
    new_role: str = "role:manager"
    update_data: UserUpdateAuthPermissions = UserUpdateAuthPermissions(
        email=user.email, principals=[new_role]
    )
    updated_user: User = await user_repo.updatePermissions(
        entry=user, schema=update_data, method="add"
    )
    assert "role:user" in updated_user.principals
    assert f"user:{user.email}" in updated_user.principals
    assert new_role in updated_user.principals


async def test_crud_update_permissions_remove(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: User = await user_repo.create(schema=user_in)
    assert user
    remove_role: str = "role:manager"
    update_data: UserUpdateAuthPermissions = UserUpdateAuthPermissions(
        email=user.email, principals=[remove_role]
    )
    updated_user: User = await user_repo.updatePermissions(
        entry=user, schema=update_data, method="remove"
    )
    assert "role:user" in updated_user.principals
    assert f"user:{user.email}" in updated_user.principals
    assert remove_role not in updated_user.principals


async def test_crud_update_permissions_remove_email_not_exists(
    db_session: AsyncSession,
) -> None:
    user_repo: UserRepository = UserRepository(session=db_session)
    fake_username: str = random_email()
    username: str = random_email()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(
        email=username, password=password, is_superuser=True
    )
    user: User = await user_repo.create(schema=user_in)
    assert user
    new_role: str = "role:admin"
    update_data: UserUpdateAuthPermissions = UserUpdateAuthPermissions(
        email=fake_username, principals=[new_role]
    )
    with pytest.raises(ApiAuthException):
        updated_user: Any = await user_repo.updatePermissions(
            entry=user, schema=update_data, method="remove"
        )
        assert not updated_user
