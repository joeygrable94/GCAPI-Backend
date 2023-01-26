from time import sleep
from typing import Any, Dict, Optional, Tuple

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import (
    create_new_user,
    create_random_user,
    get_current_user_tokens,
)
from tests.utils.utils import random_email, random_lower_string

from app.api.errors import ErrorCode
from app.core.config import settings
from app.db.schemas import UserRead, UserUpdate
from app.db.schemas.user import UserAdmin
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_get_current_superuser(
    client: AsyncClient, superuser_token_headers: Dict[str, str]
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    a_user: Dict[str, Any] = response.json()
    assert "id" in a_user
    assert a_user["email"] == settings.FIRST_SUPERUSER
    assert "hashed_password" not in a_user
    assert "password" not in a_user
    assert a_user["is_active"]
    assert a_user["is_verified"]
    assert a_user["is_superuser"]


async def test_get_current_testuser(
    client: AsyncClient, testuser_token_headers: Dict[str, str]
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=testuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    a_user: Dict[str, Any] = response.json()
    assert "id" in a_user
    assert a_user["email"] == settings.TEST_NORMAL_USER
    assert "hashed_password" not in a_user
    assert "password" not in a_user
    assert a_user["is_active"]
    assert a_user["is_verified"]
    assert not a_user["is_superuser"]


async def test_update_current_superuser(
    client: AsyncClient,
    current_superuser: Tuple[UserAdmin | UserRead, Dict[str, str]],
) -> None:
    current_user: UserAdmin | UserRead
    current_token_headers: Dict[str, str]
    current_user, current_token_headers = current_superuser
    update_dict = UserUpdate(is_verified=True)
    response: Response = await client.patch(
        "users/me", headers=current_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_user["email"] == current_user.email
    assert current_user.is_verified is True
    assert updated_user["is_verified"] is True


async def test_update_current_superuser_email_taken(
    client: AsyncClient,
    current_superuser: Tuple[UserAdmin | UserRead, Dict[str, str]],
) -> None:
    current_user: UserAdmin | UserRead
    current_token: Dict[str, str]
    current_user, current_token = current_superuser
    update_dict = UserUpdate(
        password="NEWvalidPassw0rd",
        email=settings.TEST_NORMAL_USER,
    )
    response: Response = await client.patch(
        "users/me", headers=current_token, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"] == ErrorCode.USER_ALREADY_EXISTS


async def test_update_current_superuser_password_too_short(
    client: AsyncClient,
    current_superuser: Tuple[UserAdmin | UserRead, Dict[str, str]],
) -> None:
    current_user: UserAdmin | UserRead
    current_token: Dict[str, str]
    current_user, current_token = current_superuser
    update_dict = UserUpdate(password="short")
    response: Response = await client.patch(
        "users/me", headers=current_token, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        updated_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MIN} or more characters"
    )


async def test_update_current_superuser_password_too_long(
    client: AsyncClient,
    current_superuser: Tuple[UserAdmin | UserRead, Dict[str, str]],
) -> None:
    current_user: UserAdmin | UserRead
    current_token: Dict[str, str]
    current_user, current_token = current_superuser
    new_pass: str = random_lower_string() * 10
    update_dict = UserUpdate(password=new_pass)
    response: Response = await client.patch(
        "users/me", headers=current_token, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        updated_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MAX} or less characters"
    )


async def test_update_current_testuser(
    client: AsyncClient,
    current_testuser: Tuple[UserRead, Dict[str, str]],
) -> None:
    current_user: UserRead
    current_token_headers: Dict[str, str]
    current_user, current_token_headers = current_testuser
    update_dict = UserUpdate(password="NEWvalidPassw0rd")
    sleep(1)
    response: Response = await client.patch(
        "users/me", headers=current_token_headers, json=update_dict.dict()
    )
    updated_user: UserRead = UserRead(**response.json())
    assert 200 <= response.status_code < 300
    assert not current_user.updated_on == updated_user.updated_on


async def test_update_current_testuser_email_taken(
    client: AsyncClient,
    user_auth: AuthManager,
    current_testuser: Tuple[UserRead, Dict[str, str]],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    current_user: UserRead
    current_token_headers: Dict[str, str]
    current_user, current_token_headers = current_testuser
    update_dict = UserUpdate(
        password="NEWvalidPassw0rd",
        email=a_user.email,
    )
    response: Response = await client.patch(
        "users/me", headers=current_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"] == ErrorCode.USER_ALREADY_EXISTS


async def test_list_users_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    user_1: UserAdmin = await create_random_user(user_auth)
    user_2: UserAdmin = await create_random_user(user_auth)
    response: Response = await client.get("users/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_users: Any = response.json()
    assert len(all_users) > 1
    for api_user in all_users:
        assert "email" in api_user
        assert "hashed_password" not in api_user
        if api_user["email"] == user_1.email:
            assert api_user["email"] == user_1.email
        if api_user["email"] == user_2.email:
            assert api_user["email"] == user_2.email


async def test_list_users_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    user_1: UserAdmin = await create_random_user(user_auth)  # noqa: F841
    user_2: UserAdmin = await create_random_user(user_auth)  # noqa: F841
    response: Response = await client.get("users/", headers=testuser_token_headers)
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_create_user_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    username: str = random_email()
    password: str = random_lower_string()
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    a_user: Dict[str, Any] = response.json()
    assert "id" in a_user
    assert a_user["email"] == username
    assert "hashed_password" not in a_user
    assert "password" not in a_user
    assert a_user["is_active"]
    assert not a_user["is_verified"]
    assert not a_user["is_superuser"]


async def test_create_user_as_superuser_user_already_exists(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    password: str = random_lower_string()
    data: Dict[str, str] = {"email": settings.TEST_NORMAL_USER, "password": password}
    response: Response = await client.post(
        "users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    a_user: Dict[str, Any] = response.json()
    assert a_user["detail"] == ErrorCode.USER_ALREADY_EXISTS


async def test_create_user_as_superuser_password_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    username: str = random_email()
    password: str = random_lower_string() * 10
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    a_user: Dict[str, Any] = response.json()
    assert a_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        a_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MAX} or less characters"
    )


async def test_create_user_as_superuser_password_too_short(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    username: str = random_email()
    password: str = "1234567"
    data: Dict[str, str] = {"email": username, "password": password}
    response: Response = await client.post(
        "users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 400
    a_user: Dict[str, Any] = response.json()
    assert a_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        a_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MIN} or more characters"
    )


async def test_get_user_by_id_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    user: UserAdmin = await create_random_user(user_auth)
    response: Response = await client.get(
        f"users/{user.id}",
        headers=superuser_token_headers,
    )
    fetched_user: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert fetched_user["id"] == str(user.id)
    existing_user: Any = await user_auth.users.read_by_email(user.email)
    assert existing_user
    assert existing_user.email == fetched_user["email"]


async def test_get_user_by_id_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    user: UserAdmin = await create_random_user(user_auth)
    response: Response = await client.get(
        f"users/{user.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_update_user_as_random_user_forbidden(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserAdmin
    a_user_password: str
    a_user, a_user_password = await create_new_user(user_auth)
    b_user: UserAdmin = await create_random_user(user_auth)
    update_dict = UserUpdate(
        password="NEWvalidPassw0rd",
        email=b_user.email,
    )
    a_user_access_header = await get_current_user_tokens(
        client, a_user.email, a_user_password
    )
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=a_user_access_header, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert updated_user["detail"]["code"] == 401
    assert updated_user["detail"]["reason"] == ErrorCode.TOKEN_INVALID


async def test_update_user_email_already_exists(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    b_user: UserAdmin = await create_random_user(user_auth)
    update_dict = UserUpdate(
        password="NEWvalidPassw0rd",
        email=b_user.email,
    )
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"] == ErrorCode.USER_ALREADY_EXISTS


async def test_update_user_password_too_short(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    update_dict = UserUpdate(password="short")
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        updated_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MIN} or more characters"
    )


async def test_update_user_password_too_long(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    new_pass: str = random_lower_string() * 10
    update_dict = UserUpdate(password=new_pass)
    response: Response = await client.patch(
        f"users/{a_user.id}", headers=superuser_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        updated_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MAX} or less characters"
    )


async def test_update_add_user_permissions_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    new_role = "role:manager"
    update_data = {"email": a_user.email, "principals": [new_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/add",
        headers=superuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert "role:user" in updated_user["principals"]
    assert f"user:{a_user.email}" in updated_user["principals"]
    assert new_role in updated_user["principals"]


async def test_update_add_user_permissions_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    new_role: str = "role:manager"
    update_data: Dict[str, Any] = {"email": a_user.email, "principals": [new_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/add",
        headers=testuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert updated_user["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_update_add_user_permissions_as_superuser_email_invalid(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    fake_email: str = random_email()
    update_data: Dict[str, Any] = {"email": fake_email, "principals": ["role:manager"]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/add",
        headers=superuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert updated_user["detail"] == "email must match the user to update"


async def test_update_remove_user_permissions_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    remove_role: str = "role:user"
    update_data: Dict[str, Any] = {"email": a_user.email, "principals": [remove_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/remove",
        headers=superuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert f"user:{a_user.email}" in updated_user["principals"]
    assert remove_role not in updated_user["principals"]


async def test_update_remove_user_permissions_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    remove_role: str = "role:user"
    update_data: Dict[str, Any] = {"email": a_user.email, "principals": [remove_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/remove",
        headers=testuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert updated_user["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_update_remove_user_permissions_as_superuser_email_invalid(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    remove_role: str = "role:user"
    fake_email: str = random_email()
    update_data: Dict[str, Any] = {"email": fake_email, "principals": [remove_role]}
    response: Response = await client.patch(
        f"users/{a_user.id}/permissions/remove",
        headers=superuser_token_headers,
        json=update_data,
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 401
    assert updated_user["detail"] == "email must match the user to update"


async def test_delete_user_by_id_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    user: UserAdmin = await create_random_user(user_auth)
    response: Response = await client.delete(
        f"users/{user.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    user_not_found: Optional[Any] = await user_auth.users.read_by_email(
        email=user.email
    )
    assert user_not_found is None


async def test_delete_user_by_id_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    user: UserAdmin = await create_random_user(user_auth)
    response: Response = await client.delete(
        f"users/{user.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS
