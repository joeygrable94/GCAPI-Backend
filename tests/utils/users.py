from os import environ
from typing import Dict

import requests
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_email, random_lower_string

from app.core.config import settings
from app.core.security.permissions import AclPrivilege, RoleUser
from app.crud.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate


def get_auth0_access_token(
    email: str,
    password: str,
) -> Dict[str, str]:
    url = f"https://{settings.auth.domain}/oauth/token"
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": settings.auth.audience,
        "scope": "openid profile email",
    }
    clid: str | None = environ.get("AUTH0_SPA_CLIENT_ID", None)
    clsh: str | None = environ.get("AUTH0_SPA_CLIENT_SECRET", None)
    if clid is None:
        raise ValueError("AUTH0_SPA_CLIENT_ID is not set")
    if clsh is None:
        raise ValueError("AUTH0_SPA_CLIENT_SECRET is not set")
    headers = {"content-type": "application/json"}
    response = requests.post(url, json=data, headers=headers, auth=(clid, clsh))
    data = response.json()
    access_token = data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


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
            is_active=is_active,
            is_verified=is_verified,
            is_superuser=is_superuser,
            scopes=scopes,
        )
    )
    return user
