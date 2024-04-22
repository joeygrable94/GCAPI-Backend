from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_email, random_lower_string

from app.core.security.permissions import AclPrivilege, RoleUser
from app.crud.user import UserRepository
from app.db.constants import DB_STR_USER_PICTURE_DEFAULT
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_email(
    db_session: AsyncSession,
    email: EmailStr | None = None,
) -> User:
    repo: UserRepository = UserRepository(session=db_session)
    user: User | None = await repo.read_by("email", email)
    if user is None:
        user = await create_random_user(db_session=db_session, email=email)
    return user


async def create_random_user(
    db_session: AsyncSession,
    auth_id: str | None = None,
    email: EmailStr | None = None,
    username: str | None = None,
    is_active: bool = True,
    is_verified: bool = True,
    is_superuser: bool = False,
    scopes: list[AclPrivilege] = [RoleUser],
) -> User:
    auth_id = random_lower_string(chars=30) if auth_id is None else auth_id
    email = random_email() if email is None else email
    username = random_lower_string() if username is None else username
    repo: UserRepository = UserRepository(session=db_session)
    user: User = await repo.create(
        schema=UserCreate(
            auth_id=auth_id,
            email=email,
            username=username,
            picture=DB_STR_USER_PICTURE_DEFAULT,
            is_active=is_active,
            is_verified=is_verified,
            is_superuser=is_superuser,
            scopes=scopes,
        )
    )
    return user
