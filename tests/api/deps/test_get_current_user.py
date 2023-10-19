from typing import Any, List

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_email

from app.api.deps import get_current_user, get_current_user_privileges
from app.api.exceptions import ErrorCode
from app.core.security import AclScope, Auth0User
from app.core.security.permissions import Authenticated, Everyone
from app.core.utilities.uuids import get_uuid_str
from app.models.user import User


class MockAuth:
    def __init__(self) -> None:
        self.user: Auth0User

    async def __call__(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return self

    async def get_user(self) -> Auth0User:
        return self.user

    def set_user(self, user: dict) -> None:
        self.user = Auth0User(**user)


@pytest.fixture
def auth() -> MockAuth:
    mock_auth = MockAuth()
    mock_auth.set_user(
        {
            "sub": get_uuid_str(),
            "https://github.com/dorinclisu/fastapi-auth0/email": random_email(),
            "https://github.com/dorinclisu/fastapi-auth0/roles": ["user", "employee"],
            "permissions": ["access:test"],
        }
    )
    return mock_auth


async def test_get_current_user(db_session: AsyncSession, auth: MockAuth) -> None:
    # Test with a valid user
    user: Auth0User = await auth.get_user()
    user_in_db: User = await get_current_user(db_session, user)
    assert user.auth_id == user_in_db.auth_id

    # Test with None
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(db_session, None)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == ErrorCode.UNAUTHORIZED


async def test_get_current_user_privileges(
    db_session: AsyncSession, auth: MockAuth
) -> None:
    # Test with a valid user
    user: Auth0User = await auth.get_user()
    user_in_db: User = await get_current_user(db_session, user)
    if user_in_db:
        principals: List[AclScope] = get_current_user_privileges(user_in_db)
        assert len(principals) == 6
        assert Everyone in principals
        assert Authenticated in principals
        assert AclScope(scope="role:user") in principals
        assert AclScope(scope="role:employee") in principals
