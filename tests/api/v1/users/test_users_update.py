from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import create_random_user
from tests.utils.utils import random_lower_string

from app.core.config import settings
from app.crud import UserRepository
from app.models import User
from app.schemas import UserUpdate, UserUpdateAsManager
from app.schemas.user import UserRead

pytestmark = pytest.mark.asyncio


# async def test_update_user_self_admin(
#     client: AsyncClient,
#     db_session: AsyncSession,
#     admin_token_headers: Dict[str, str],
# ):
#     user_1 = create_random_user(db_session=db_session)


# async def test_update_user_self_manager():


async def test_update_user_self_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    employee1: User | None = await user_repo.read_by(
        "email", settings.auth.first_employee
    )
    assert employee1 is not None
    new_username: str = random_lower_string()
    update_dict: UserUpdate = UserUpdate(username=new_username)
    # can access self
    response: Response = await client.patch(
        f"users/{employee1.id}",
        headers=employee_token_headers,
        json=update_dict.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    employee1_new: UserRead = UserRead.model_validate(data)
    assert 200 <= response.status_code < 300
    assert employee1_new.username == new_username


async def test_update_user_self_employee_invalid_update(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    employee1: User | None = await user_repo.read_by(
        "email", settings.auth.first_employee
    )
    assert employee1 is not None
    new_username: str = random_lower_string()
    update_dict: UserUpdateAsManager = UserUpdateAsManager(
        username=new_username, is_active=True
    )
    # can access self
    response: Response = await client.patch(
        f"users/{employee1.id}",
        headers=employee_token_headers,
        json=update_dict.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert (
        data["detail"]
        == "You do not have permission to take this action on this resource"
    )


# async def test_update_user_as_admin():


# async def test_update_user_as_manager():


async def test_update_user_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    user_1: User = await create_random_user(db_session=db_session)
    new_username: str = random_lower_string()
    update_dict: UserUpdate = UserUpdate(username=new_username)
    # can access self
    response: Response = await client.patch(
        f"users/{user_1.id}",
        headers=employee_token_headers,
        json=update_dict.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Insufficient permissions"
