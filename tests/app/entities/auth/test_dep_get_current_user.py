from datetime import datetime
from typing import Any, Generator, List

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_USER_PICTURE_DEFAULT
from app.entities.auth.constants import ERROR_MESSAGE_UNAUTHORIZED
from app.entities.auth.dependencies import get_current_user, get_current_user_privileges
from app.services.clerk.schemas import ClerkUser
from app.services.permission import AclPrivilege, Authenticated, Everyone
from app.utilities import get_uuid_str
from app.utilities.uuids import get_random_username
from tests.utils.utils import random_email, random_lower_string


class MockAuth:
    def __init__(self) -> None:
        self.user: ClerkUser

    async def __call__(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return self

    async def get_user(self) -> ClerkUser:
        return self.user

    def set_user(self, user: dict) -> None:
        self.user = ClerkUser(**user)


@pytest.fixture(scope="module")
def auth() -> Generator[MockAuth, None, None]:
    mock_auth = MockAuth()
    mock_auth.set_user(
        {
            "user_id": "user_" + get_uuid_str().replace("-", ""),
            "email": random_email(),
            "first_name": random_lower_string(16),
            "last_name": random_lower_string(16),
            "username": get_random_username(),
            "picture": DB_STR_USER_PICTURE_DEFAULT,
            "is_verified": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    )
    yield mock_auth


async def test_get_current_user(db_session: AsyncSession, auth: MockAuth) -> None:
    user: ClerkUser = await auth.get_user()
    user_in_db = await get_current_user(db_session, user)
    assert user.auth_id == user_in_db.auth_id
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(db_session, None)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == ERROR_MESSAGE_UNAUTHORIZED


async def test_get_current_user_privileges(
    db_session: AsyncSession, auth: MockAuth
) -> None:
    user: ClerkUser = await auth.get_user()
    user_in_db = await get_current_user(db_session, user)
    if user_in_db:
        principals: List[AclPrivilege] = get_current_user_privileges(user_in_db)
        assert len(principals) == 4
        assert Everyone in principals
        assert Authenticated in principals
        assert AclPrivilege("role:user") in principals
