import asyncio
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import config as settings
from app.core import crud
from app.core.crud.make_user import create_user
from app.core.models.user import User
from app.core.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


async def user_authentication_headers(
    *,
    client: TestClient,
    email: str,
    password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}
    r = await client.post(f"{settings.API_VERSION}/auth/jwt/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def create_random_user(db: AsyncSession) -> User:
    email = random_email()
    password = random_lower_string()
    user = await create_user(email, password, False)
    return user


# async def authentication_token_from_email(
#     *, client: TestClient, email: str, db: AsyncSession
# ) -> Dict[str, str]:
#     """
#     Return a valid token for the user with given email.
#     If the user doesn't exist it is created first.
#     """
#     password = random_lower_string()
#     user = await crud.user.get_by_email(db, email=email)
#     if not user:
#         user = await create_user(email, password, False)
#         # user_in_create = UserCreate(username=email, email=email, password=password)
#         # user = await crud.user.create(db, obj_in=user_in_create)
#     else:
#         user_in_update = UserUpdate(password=password)
#         user = await crud.user.update(db, db_obj=user, obj_in=user_in_update)
#     return user_authentication_headers(client=client, email=email, password=password)
