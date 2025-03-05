from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import ERROR_MESSAGE_ID_INVALID
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.core_user.constants import (
    ERROR_MESSAGE_USER_NOT_FOUND,
    ERROR_MESSAGE_USERNAME_EXISTS,
)
from app.entities.core_user.crud import UserRepository
from app.entities.core_user.model import User
from app.entities.core_user.schemas import (
    UserDelete,
    UserRead,
    UserReadAsAdmin,
    UserReadAsManager,
    UserUpdate,
    UserUpdateAsAdmin,
    UserUpdateAsManager,
    UserUpdatePrivileges,
)
from app.services.clerk.settings import clerk_settings
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_SCOPE_ADD,
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_SCOPE_REMOVE,
)
from app.services.permission.schemas import AclPrivilege
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.users import create_random_user
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.anyio


async def perform_test_list(
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
    is_superuser: bool = False,
    is_manager: bool = False,
) -> None:
    response: Response = await client.get(
        "users/",
        headers=current_user.token_headers,
    )
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 7
    assert data["size"] == 1000
    assert len(data["results"]) == 7
    for entry in data["results"]:
        assert "id" in entry
        assert "auth_id" in entry
        assert "email" in entry
        assert "is_active" in entry
        assert "is_verified" in entry
        if is_manager:
            assert "scopes" in entry
        if is_superuser:
            assert "is_superuser" in entry


async def perform_test_current(
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get(
        "users/me",
        headers=current_user.token_headers,
    )
    entry = response.json()
    data = UserRead.model_validate(entry)
    assert 200 <= response.status_code < 300
    assert data.id
    user_repo = UserRepository(db_session)
    existing_data = await user_repo.read_by("auth_id", data.auth_id)
    assert existing_data
    assert existing_data.email == data.email


class TestReadCurrentUser:
    # AUTHORIZED CLIENTS
    async def test_read_current_user_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_current(client, db_session, admin_user)

    async def test_read_current_user_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_current(client, db_session, manager_user)

    async def test_read_current_user_as_employee_user(
        self, client, db_session, employee_user
    ) -> None:
        await perform_test_current(client, db_session, employee_user)

    async def test_read_current_user_as_client_a_user(
        self, client, db_session, client_a_user
    ) -> None:
        await perform_test_current(client, db_session, client_a_user)

    async def test_read_current_user_as_client_b_user(
        self, client, db_session, client_b_user
    ) -> None:
        await perform_test_current(client, db_session, client_b_user)

    async def test_read_current_user_as_verified_user(
        self, client, db_session, verified_user
    ) -> None:
        await perform_test_current(client, db_session, verified_user)

    # CASES
    async def test_read_current_user_unverified(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        unverified_user: ClientAuthorizedUser,
    ) -> None:
        response: Response = await client.get(
            "users/me",
            headers=unverified_user.token_headers,
        )
        json_data: dict[str, Any] = response.json()
        assert response.status_code == 403
        assert json_data["detail"] == ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED


class TestListUsers:
    # AUTHORIZED CLIENTS
    async def test_list_all_users_as_admin(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_list(
            client, db_session, admin_user, is_superuser=True, is_manager=True
        )

    async def test_list_all_users_as_manager(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_list(
            client, db_session, manager_user, is_superuser=False, is_manager=True
        )

    # CASES
    async def test_list_all_users_as_employee(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        response: Response = await client.get(
            "users/",
            headers=employee_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS
        assert response.status_code == 405


class TestReadUsers:
    # CASES
    async def test_read_all_users_as_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        user = await create_random_user(db_session)
        response: Response = await client.get(
            f"users/{user.id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert 200 <= response.status_code < 300
        assert data["id"] == str(user.id)
        assert data.get("scopes") is not None
        assert data.get("is_superuser") is not None

    async def test_read_all_users_as_manager(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        user = await create_random_user(db_session)
        response: Response = await client.get(
            f"users/{user.id}",
            headers=manager_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert 200 <= response.status_code < 300
        assert data["id"] == str(user.id)
        assert data.get("scopes") is not None
        assert data.get("is_superuser") is None

    async def test_read_user_as_employee(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        user_repo = UserRepository(db_session)
        user_employee = await user_repo.read_by("email", clerk_settings.first_employee)
        user_client_a = await user_repo.read_by("email", clerk_settings.first_client_a)
        assert user_employee is not None
        assert user_client_a is not None
        # can access self
        response: Response = await client.get(
            f"users/{user_employee.id}",
            headers=employee_user.token_headers,
        )
        data_a: dict[str, Any] = response.json()
        assert 200 <= response.status_code < 300
        assert data_a["id"] == str(user_employee.id)
        assert data_a.get("scopes") is None
        assert data_a.get("is_superuser") is None
        # cannot access other users
        response_b: Response = await client.get(
            f"users/{user_client_a.id}",
            headers=employee_user.token_headers,
        )
        data_b: dict[str, Any] = response_b.json()
        assert data_b["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS
        assert response_b.status_code == 403

    async def test_read_user_as_user_verified(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        verified_user: ClientAuthorizedUser,
    ) -> None:
        user_repo = UserRepository(db_session)
        user_employee = await user_repo.read_by("email", clerk_settings.first_employee)
        user_verified = await user_repo.read_by(
            "email", clerk_settings.first_user_verified
        )
        assert user_employee is not None
        assert user_verified is not None
        # can access self
        response: Response = await client.get(
            f"users/{user_verified.id}",
            headers=verified_user.token_headers,
        )
        data_a: dict[str, Any] = response.json()
        assert 200 <= response.status_code < 300
        assert data_a["id"] == str(user_verified.id)
        assert data_a.get("scopes") is None
        assert data_a.get("is_superuser") is None
        # cannot access other users
        response_b: Response = await client.get(
            f"users/{user_employee.id}",
            headers=verified_user.token_headers,
        )
        data_b: dict[str, Any] = response_b.json()
        assert data_b["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS
        assert response_b.status_code == 403

    async def test_read_user_by_id_as_admin_user_not_found(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        fake_id = get_uuid_str()
        response: Response = await client.get(
            f"users/{fake_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert data["detail"] == ERROR_MESSAGE_USER_NOT_FOUND

    async def test_read_user_by_id_as_admin_id_invalid(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        fake_id = "FAKE-UUID-ASDF-1234567890"
        response: Response = await client.get(
            f"users/{fake_id}",
            headers=admin_user.token_headers,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 422
        assert data["detail"] == ERROR_MESSAGE_ID_INVALID


class TestUpdateUsers:
    async def test_update_user_self_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        user_repo = UserRepository(db_session)
        admin1 = await user_repo.read_by("email", clerk_settings.first_admin)
        assert admin1 is not None
        assert admin1.is_active is True
        assert admin1.is_superuser is True
        new_username: str = random_lower_string()
        update_dict = UserUpdateAsAdmin(username=new_username, is_active=False)
        response: Response = await client.patch(
            f"users/{admin1.id}",
            headers=admin_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        admin1_new = UserReadAsAdmin.model_validate(data)
        assert 200 <= response.status_code < 300
        assert admin1_new.username == new_username
        assert admin1_new.is_active is False
        assert admin1_new.is_verified is True
        update_dict2 = UserUpdateAsAdmin(is_active=True)
        response_revert: Response = await client.patch(
            f"users/{admin1.id}",
            headers=admin_user.token_headers,
            json=update_dict2.model_dump(),
        )
        data_revert: dict[str, Any] = response_revert.json()
        assert 200 <= response_revert.status_code < 300
        assert data_revert["is_active"] is True
        assert data_revert["is_verified"] is True

    async def test_update_user_self_manager(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        user_repo = UserRepository(db_session)
        manager1 = await user_repo.read_by("email", clerk_settings.first_manager)
        assert manager1 is not None
        assert manager1.is_active is True
        new_username: str = random_lower_string()
        update_dict = UserUpdateAsManager(username=new_username, is_active=False)
        response: Response = await client.patch(
            f"users/{manager1.id}",
            headers=manager_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        manager1_new = UserReadAsManager.model_validate(data)
        assert 200 <= response.status_code < 300
        assert manager1_new.username == new_username
        assert manager1_new.is_active is False
        response_revert: Response = await client.patch(
            f"users/{manager1.id}",
            headers=manager_user.token_headers,
            json=UserUpdateAsManager(is_active=True).model_dump(),
        )
        assert 200 <= response_revert.status_code < 300
        data_revert: dict[str, Any] = response_revert.json()
        manager1_revert = UserReadAsManager.model_validate(data_revert)
        assert manager1_revert.is_active is True

    async def test_update_user_self_manager_invalid_update_obj(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        user_repo = UserRepository(db_session)
        manager1 = await user_repo.read_by("email", clerk_settings.first_manager)
        assert manager1 is not None
        assert manager1.is_active is True
        new_username: str = random_lower_string()
        update_dict = UserUpdateAsAdmin(
            username=new_username, is_active=False, is_superuser=True
        )
        response: Response = await client.patch(
            f"users/{manager1.id}",
            headers=manager_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 405
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION

    async def test_update_user_self_employee(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        user_repo = UserRepository(db_session)
        employee1 = await user_repo.read_by("email", clerk_settings.first_employee)
        assert employee1 is not None
        new_username: str = random_lower_string()
        update_dict = UserUpdate(username=new_username)
        response: Response = await client.patch(
            f"users/{employee1.id}",
            headers=employee_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        employee1_new = UserRead.model_validate(data)
        assert 200 <= response.status_code < 300
        assert employee1_new.username == new_username

    async def test_update_user_self_employee_invalid_update_obj(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        user_repo = UserRepository(db_session)
        employee1 = await user_repo.read_by("email", clerk_settings.first_employee)
        assert employee1 is not None
        new_username: str = random_lower_string()
        update_dict = UserUpdateAsManager(username=new_username, is_active=True)
        response: Response = await client.patch(
            f"users/{employee1.id}",
            headers=employee_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 405
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION

    async def test_update_other_user_as_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        user1 = await create_random_user(db_session=db_session)
        new_username: str = random_lower_string()
        update_dict = UserUpdateAsAdmin(
            username=new_username,
            is_active=False,
            is_superuser=True,
        )
        response: Response = await client.patch(
            f"users/{user1.id}",
            headers=admin_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        user1_new = UserReadAsAdmin.model_validate(data)
        assert 200 <= response.status_code < 300
        assert user1_new.username == new_username
        assert user1_new.is_active is False
        assert user1_new.is_superuser is True

    async def test_update_other_user_as_admin_username_taken(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        user1 = await create_random_user(db_session=db_session)
        user2 = await create_random_user(db_session=db_session)
        new_username: str = random_lower_string()
        user_1_update_dict = UserUpdate(username=new_username)
        user1_response: Response = await client.patch(
            f"users/{user1.id}",
            headers=admin_user.token_headers,
            json=user_1_update_dict.model_dump(),
        )
        data: dict[str, Any] = user1_response.json()
        user1_new = UserReadAsAdmin.model_validate(data)
        assert 200 <= user1_response.status_code < 300
        assert user1_new.username == new_username
        user2_response: Response = await client.patch(
            f"users/{user2.id}",
            headers=admin_user.token_headers,
            json=user_1_update_dict.model_dump(),
        )
        data: dict[str, Any] = user2_response.json()
        assert user2_response.status_code == 400
        assert data["detail"] == ERROR_MESSAGE_USERNAME_EXISTS

    async def test_update_other_user_as_manager(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        user1 = await create_random_user(db_session=db_session)
        new_username: str = random_lower_string()
        update_dict = UserUpdateAsManager(
            username=new_username,
            is_active=False,
            is_verified=False,
        )
        response: Response = await client.patch(
            f"users/{user1.id}",
            headers=manager_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        user1_new = UserReadAsManager.model_validate(data)
        assert 200 <= response.status_code < 300
        assert user1_new.username == new_username
        assert user1_new.is_active is False
        assert user1_new.is_verified is False

    async def test_update_other_user_as_manager_invalid_update_obj(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        user1 = await create_random_user(db_session=db_session)
        new_username: str = random_lower_string()
        update_dict = UserUpdateAsAdmin(
            username=new_username,
            is_active=False,
            is_superuser=True,
        )
        response: Response = await client.patch(
            f"users/{user1.id}",
            headers=manager_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 405
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION

    async def test_update_other_user_as_employee(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        user_1 = await create_random_user(db_session=db_session)
        new_username: str = random_lower_string()
        update_dict = UserUpdate(username=new_username)
        response: Response = await client.patch(
            f"users/{user_1.id}",
            headers=employee_user.token_headers,
            json=update_dict.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 403
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS


class TestDeleteUsers:
    async def test_delete_other_user_as_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        user1: User = await create_random_user(db_session=db_session)
        response: Response = await client.delete(
            f"users/{user1.id}", headers=admin_user.token_headers
        )
        data: dict[str, Any] = response.json()
        user_deleted: UserDelete = UserDelete.model_validate(data)
        assert user_deleted.message == "User deleted"
        assert user_deleted.user_id == user1.id

    async def test_delete_other_user_as_manager(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        user1: User = await create_random_user(db_session=db_session)
        response: Response = await client.delete(
            f"users/{user1.id}", headers=manager_user.token_headers
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 405
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS

    async def test_delete_user_request_to_delete_self(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        verified_user: ClientAuthorizedUser,
    ) -> None:
        user_repo: UserRepository = UserRepository(db_session)
        verified1: User | None = await user_repo.read_by(
            "email", clerk_settings.first_user_verified
        )
        assert verified1
        response: Response = await client.delete(
            f"users/{verified1.id}", headers=verified_user.token_headers
        )
        data: dict[str, Any] = response.json()
        assert 200 <= response.status_code < 300
        assert data["message"] == "User requested to be deleted"
        assert data["user_id"] == str(verified1.id)


class TestAddPrivilegesToUsers:
    async def test_add_user_priv_as_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        user1 = await create_random_user(db_session=db_session)
        test_priv = AclPrivilege("test:priv1")
        user1_update_priv: dict[str, Any] = {"scopes": [test_priv]}
        response: Response = await client.post(
            f"users/{user1.id}/privileges/add",
            headers=admin_user.token_headers,
            json=user1_update_priv,
        )
        assert 200 <= response.status_code < 300
        data: dict[str, Any] = response.json()
        assert test_priv in data["scopes"]

    async def test_add_user_priv_as_manager(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        user1 = await create_random_user(db_session=db_session)
        test_priv = AclPrivilege("test:priv1")
        user1_update_priv: dict[str, Any] = {"scopes": [test_priv]}
        response: Response = await client.post(
            f"users/{user1.id}/privileges/add",
            headers=manager_user.token_headers,
            json=user1_update_priv,
        )
        assert 200 <= response.status_code < 300
        data: dict[str, Any] = response.json()
        assert test_priv in data["scopes"]

    async def test_add_user_priv_as_manager_add_role_disallowed(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        user1 = await create_random_user(db_session=db_session)
        test_priv = AclPrivilege("role:admin")
        user1_update_priv: dict[str, Any] = {"scopes": [test_priv]}
        response: Response = await client.post(
            f"users/{user1.id}/privileges/add",
            headers=manager_user.token_headers,
            json=user1_update_priv,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 405
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_SCOPE_ADD

    async def test_add_user_priv_as_user_disallowed(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        user1 = await create_random_user(db_session=db_session)
        test_priv = AclPrivilege("role:admin")
        user1_update_priv: dict[str, Any] = {"scopes": [test_priv]}
        response: Response = await client.post(
            f"users/{user1.id}/privileges/add",
            headers=employee_user.token_headers,
            json=user1_update_priv,
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 403
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS


class TestRemovePrivilegesToUsers:
    async def test_remove_user_priv_as_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        test_priv1 = AclPrivilege("test:priv1")
        test_priv2 = AclPrivilege("test:priv2")
        user1 = await create_random_user(
            db_session=db_session, scopes=[test_priv1, test_priv2]
        )
        user1_remove_priv = UserUpdatePrivileges(scopes=[test_priv2])
        response: Response = await client.post(
            f"users/{user1.id}/privileges/remove",
            headers=admin_user.token_headers,
            json=user1_remove_priv.model_dump(),
        )
        data: dict[str, Any] = response.json()
        user1_new = UserReadAsAdmin.model_validate(data)
        assert 200 <= response.status_code < 300
        assert test_priv1 in user1_new.scopes
        assert test_priv2 not in user1_new.scopes

    async def test_remove_user_priv_as_manager(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        test_priv1 = AclPrivilege("test:priv1")
        test_priv2 = AclPrivilege("test:priv2")
        user1 = await create_random_user(
            db_session=db_session, scopes=[test_priv1, test_priv2]
        )
        user1_remove_priv = UserUpdatePrivileges(scopes=[test_priv2])
        response: Response = await client.post(
            f"users/{user1.id}/privileges/remove",
            headers=manager_user.token_headers,
            json=user1_remove_priv.model_dump(),
        )
        data: dict[str, Any] = response.json()
        user1_new = UserReadAsManager.model_validate(data)
        assert 200 <= response.status_code < 300
        assert test_priv1 in user1_new.scopes
        assert test_priv2 not in user1_new.scopes

    async def test_remove_user_priv_as_manager_add_role_disallowed(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        manager_user: ClientAuthorizedUser,
    ) -> None:
        test_priv1 = AclPrivilege("test:priv1")
        test_priv2 = AclPrivilege("test:priv2")
        test_role1 = AclPrivilege("role:organization")
        user1 = await create_random_user(
            db_session=db_session, scopes=[test_role1, test_priv1, test_priv2]
        )
        user1_remove_priv = UserUpdatePrivileges(scopes=[test_role1])
        response: Response = await client.post(
            f"users/{user1.id}/privileges/remove",
            headers=manager_user.token_headers,
            json=user1_remove_priv.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 405
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_SCOPE_REMOVE

    async def test_remove_user_priv_as_user_disallowed(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        test_priv1 = AclPrivilege("test:priv1")
        test_priv2 = AclPrivilege("test:priv2")
        user1 = await create_random_user(
            db_session=db_session, scopes=[test_priv1, test_priv2]
        )
        user1_remove_priv = UserUpdatePrivileges(scopes=[test_priv2])
        response: Response = await client.post(
            f"users/{user1.id}/privileges/remove",
            headers=employee_user.token_headers,
            json=user1_remove_priv.model_dump(),
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 403
        assert data["detail"] == ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS
