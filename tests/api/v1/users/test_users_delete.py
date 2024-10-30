from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import create_random_user

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.crud import UserRepository
from app.models import User
from app.schemas import UserDelete

pytestmark = pytest.mark.asyncio


async def test_delete_other_user_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    response: Response = await client.delete(
        f"users/{user1.id}", headers=admin_token_headers
    )
    data: Dict[str, Any] = response.json()
    user_deleted: UserDelete = UserDelete.model_validate(data)
    assert user_deleted.message == "User deleted"
    assert user_deleted.user_id == user1.id


async def test_delete_other_user_as_manager(
    client: AsyncClient,
    db_session: AsyncSession,
    manager_token_headers: Dict[str, str],
) -> None:
    user1: User = await create_random_user(db_session=db_session)
    response: Response = await client.delete(
        f"users/{user1.id}", headers=manager_token_headers
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert data["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_delete_user_request_to_delete_self(
    client: AsyncClient,
    db_session: AsyncSession,
    user_verified_token_headers: Dict[str, str],
) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    verified1: User | None = await user_repo.read_by(
        "email", settings.auth.first_user_verified
    )
    assert verified1
    response: Response = await client.delete(
        f"users/{verified1.id}", headers=user_verified_token_headers
    )
    data: Dict[str, Any] = response.json()
    user_deleted: UserDelete = UserDelete.model_validate(data)
    assert 200 <= response.status_code < 300
    assert user_deleted.message == "User requested to be deleted"
    assert user_deleted.user_id == verified1.id
