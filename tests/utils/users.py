from typing import Literal

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_USER_PICTURE_DEFAULT
from app.entities.core_user.crud import UserRepository
from app.entities.core_user.model import User
from app.entities.core_user.schemas import (
    UserCreate,
    UserUpdateAsAdmin,
    UserUpdatePrivileges,
)
from app.services.clerk.settings import clerk_settings
from app.services.permission import AclPrivilege, RoleUser
from app.utilities.uuids import get_uuid_str
from tests.utils.utils import random_email, random_lower_string


async def get_user_by_email(
    db_session: AsyncSession,
    email: EmailStr | None = None,
) -> User:
    repo: UserRepository = UserRepository(session=db_session)
    user: User | None = await repo.read_by("email", email)
    if user is None:
        user = await create_random_user(db_session=db_session, email=email)
    return user


async def get_user_by_auth_id(db_session: AsyncSession, auth_id: str) -> User | None:
    repo: UserRepository = UserRepository(session=db_session)
    user: User | None = await repo.read_by("auth_id", auth_id)
    assert user is not None
    return user


async def create_random_user(
    db_session: AsyncSession,
    auth_id: str | None = None,
    email: EmailStr | None = None,
    username: str | None = None,
    picture: str | None = None,
    is_active: bool = True,
    is_verified: bool = False,
    is_superuser: bool = False,
    scopes: list[AclPrivilege] = [RoleUser],
) -> User:
    repo: UserRepository = UserRepository(session=db_session)
    user: User | None = await repo.read_by("auth_id", auth_id)
    if user is not None:
        user = await repo.update(
            entry=user,
            schema=UserUpdateAsAdmin(
                is_active=is_active,
                is_verified=is_verified,
                is_superuser=is_superuser,
            ),
        )
        user = await repo.add_privileges(
            entry=user,
            schema=UserUpdatePrivileges(scopes=scopes),
        )
        return user
    auth_id = random_lower_string(chars=30) if auth_id is None else auth_id
    email = random_email() if email is None else email
    username = random_lower_string() if username is None else username
    user: User = await repo.create(
        schema=UserCreate(
            auth_id=auth_id,
            email=email,
            username=username,
            picture=picture or DB_STR_USER_PICTURE_DEFAULT,
            is_active=is_active,
            is_verified=is_verified,
            is_superuser=is_superuser,
            scopes=scopes,
        )
    )
    return user


async def create_core_user(
    db_session,
    user_role: Literal[
        "admin", "manager", "employee", "client_a", "client_b", "verified", "unverified"
    ],
) -> User:
    if user_role == "admin":
        return await create_random_user(
            db_session,
            auth_id=clerk_settings.first_admin_auth_id,
            email=clerk_settings.first_admin,
            username=clerk_settings.first_admin.split("@")[0] + get_uuid_str()[:4],
            picture=clerk_settings.first_admin_picture,
            is_active=True,
            is_verified=True,
            is_superuser=True,
            scopes=[
                AclPrivilege("role:user"),
                AclPrivilege("role:admin"),
                AclPrivilege("access:test"),
            ],
        )
    if user_role == "manager":
        return await create_random_user(
            db_session,
            auth_id=clerk_settings.first_manager_auth_id,
            email=clerk_settings.first_manager,
            username=clerk_settings.first_manager.split("@")[0] + get_uuid_str()[:4],
            picture=clerk_settings.first_manager_picture,
            is_active=True,
            is_verified=True,
            is_superuser=False,
            scopes=[
                AclPrivilege("role:user"),
                AclPrivilege("role:manager"),
                AclPrivilege("access:test"),
            ],
        )
    if user_role == "employee":
        return await create_random_user(
            db_session,
            auth_id=clerk_settings.first_employee_auth_id,
            email=clerk_settings.first_employee,
            username=clerk_settings.first_employee.split("@")[0] + get_uuid_str()[:4],
            picture=clerk_settings.first_employee_picture,
            is_active=True,
            is_verified=True,
            is_superuser=False,
            scopes=[
                AclPrivilege("role:user"),
                AclPrivilege("role:employee"),
            ],
        )
    if user_role == "client_a":
        return await create_random_user(
            db_session,
            auth_id=clerk_settings.first_client_a_auth_id,
            email=clerk_settings.first_client_a,
            username=clerk_settings.first_client_a.split("@")[0] + get_uuid_str()[:4],
            picture=clerk_settings.first_client_a_picture,
            is_active=True,
            is_verified=True,
            is_superuser=False,
            scopes=[
                AclPrivilege("role:user"),
                AclPrivilege("role:organization"),
            ],
        )
    if user_role == "client_b":
        return await create_random_user(
            db_session,
            auth_id=clerk_settings.first_client_b_auth_id,
            email=clerk_settings.first_client_b,
            username=clerk_settings.first_client_b.split("@")[0] + get_uuid_str()[:4],
            picture=clerk_settings.first_client_b_picture,
            is_active=True,
            is_verified=True,
            is_superuser=False,
            scopes=[
                AclPrivilege("role:user"),
                AclPrivilege("role:organization"),
            ],
        )
    if user_role == "verified":
        return await create_random_user(
            db_session,
            email=clerk_settings.first_user_verified,
            auth_id=clerk_settings.first_user_verified_auth_id,
            username=clerk_settings.first_user_verified.split("@")[0]
            + get_uuid_str()[:4],
            picture=clerk_settings.default_picture,
            is_active=True,
            is_verified=True,
            is_superuser=False,
            scopes=[
                AclPrivilege("role:user"),
            ],
        )
    if user_role == "unverified":
        return await create_random_user(
            db_session,
            auth_id=clerk_settings.first_user_verified_auth_id,
            email=clerk_settings.first_user_verified,
            username=clerk_settings.first_user_verified.split("@")[0]
            + get_uuid_str()[:4],
            picture=clerk_settings.default_picture,
            is_active=True,
            is_verified=False,
            is_superuser=False,
            scopes=[
                AclPrivilege("role:user"),
            ],
        )
    raise ValueError("Invalid user role")
