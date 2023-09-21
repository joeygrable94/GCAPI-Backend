from typing import Any, List

import pytest
from fastapi import HTTPException, status
from fastapi_auth0 import Auth0User
from fastapi_permissions import Authenticated  # type: ignore
from fastapi_permissions import Everyone

from app.api.deps import get_current_user, get_current_user_permissions
from app.api.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str


class MockAuth:
    def __init__(self) -> None:
        self.user: Any = None

    async def __call__(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        return self

    async def get_user(self) -> Auth0User | None:
        if self.user is None:
            return None
        return Auth0User(
            sub=self.user["id"],  # type: ignore
            permissions=self.user.get("permissions"),
            email=self.user.get("email"),
        )

    def set_user(self, user: dict) -> None:
        self.user = user


@pytest.fixture
def auth() -> MockAuth:
    mock_auth = MockAuth()
    mock_auth.set_user(
        dict(
            id=get_uuid_str(),
            permissions=["permission1", "permission2"],
            email="test@getcommunity.com",
        )
    )
    return mock_auth


async def test_get_current_user(auth: MockAuth) -> None:
    # Test with a valid user
    user: Auth0User | None = await auth.get_user()
    assert get_current_user(user) == user

    # Test with None
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(None)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == ErrorCode.UNAUTHORIZED


async def test_get_current_user_permissions(auth: MockAuth) -> None:
    # Test with a valid user
    user: Auth0User | None = await auth.get_user()
    if user:
        principals: List[Any] = get_current_user_permissions(user)
        assert len(principals) == 4
        assert Everyone in principals
        assert Authenticated in principals
        assert "permission1" in principals
        assert "permission2" in principals

    # Test with None
    principals_t2: List[Any] = get_current_user_permissions(None)  # type: ignore
    assert len(principals_t2) == 1
    assert Everyone in principals_t2
