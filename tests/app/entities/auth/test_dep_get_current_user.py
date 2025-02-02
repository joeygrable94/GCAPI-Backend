from typing import Any, List

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.auth.constants import ERROR_MESSAGE_UNAUTHORIZED
from app.entities.auth.dependencies import get_current_user, get_current_user_privileges
from app.services.auth0.schemas import AuthUser
from app.services.permission import AclPrivilege, Authenticated, Everyone
from app.utilities import get_uuid_str
from tests.utils.utils import random_email


class MockAuth:
    def __init__(self) -> None:
        self.user: AuthUser

    async def __call__(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return self

    async def get_user(self) -> AuthUser:
        return self.user

    def set_user(self, user: dict) -> None:
        self.user = AuthUser(**user)


@pytest.fixture
def auth() -> MockAuth:
    mock_auth = MockAuth()
    mock_auth.set_user(
        {
            "sub": get_uuid_str(),
            "gcapi_oauth2/email": random_email(),
            "gcapi_oauth2/roles": [
                "role:user",
                "role:employee",
            ],
            "permissions": ["access:test"],
        }
    )
    return mock_auth


async def test_get_current_user(db_session: AsyncSession, auth: MockAuth) -> None:
    user: AuthUser = await auth.get_user()
    user_in_db = await get_current_user(db_session, user)
    assert user.auth_id == user_in_db.auth_id
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(db_session, None)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == ERROR_MESSAGE_UNAUTHORIZED


async def test_get_current_user_privileges(
    db_session: AsyncSession, auth: MockAuth
) -> None:
    user: AuthUser = await auth.get_user()
    user_in_db = await get_current_user(db_session, user)
    if user_in_db:
        principals: List[AclPrivilege] = get_current_user_privileges(user_in_db)
        assert len(principals) == 6
        assert Everyone in principals
        assert Authenticated in principals
        assert AclPrivilege("role:user") in principals
        assert AclPrivilege("role:employee") in principals
