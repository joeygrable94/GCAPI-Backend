from hashlib import sha1
from os import urandom
from typing import Any

import pytest
from httpx import AsyncClient, Headers, Response
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.services.csrf import csrf_settings
from app.services.encryption.schemas import EncryptedMessage, PlainMessage
from app.utilities import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.utils import random_lower_string


async def perform_status_test(
    client_user: ClientAuthorizedUser, status_code: int, client: AsyncClient
) -> None:
    response = await client.get("/status", headers=client_user.token_headers)
    assert response.status_code == status_code


class TestPublicSecureRoutes:
    # ENCRYPTION
    async def test_encrypt_decrypt_message_as_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        input_message = PlainMessage(message=random_lower_string())
        response: Response = await client.post(
            "/encrypt/message",
            headers=admin_user.token_headers,
            json=input_message.model_dump(),
        )
        data: dict[str, Any] = response.json()
        encrypted_message = EncryptedMessage.model_validate(data)
        assert 200 <= response.status_code < 300
        assert encrypted_message.message != input_message.message
        response_2: Response = await client.post(
            "/decrypt/message",
            headers=admin_user.token_headers,
            json=encrypted_message.model_dump(),
        )
        data_2: dict[str, Any] = response_2.json()
        decrypted_message = PlainMessage.model_validate(data_2)
        assert 200 <= response_2.status_code < 300
        assert decrypted_message.message == input_message.message

    # AUTHORIZED STATUS
    async def test_public_status_as_admin_user(
        self, admin_user: ClientAuthorizedUser, client: AsyncClient
    ) -> None:
        await perform_status_test(admin_user, 200, client)

    async def test_public_status_as_manager_user(
        self, manager_user: ClientAuthorizedUser, client: AsyncClient
    ) -> None:
        await perform_status_test(manager_user, 200, client)

    async def test_public_status_as_employee_user(
        self, employee_user: ClientAuthorizedUser, client: AsyncClient
    ) -> None:
        await perform_status_test(employee_user, 200, client)

    async def test_public_status_as_client_a_user(
        self, client_a_user: ClientAuthorizedUser, client: AsyncClient
    ) -> None:
        await perform_status_test(client_a_user, 200, client)

    async def test_public_status_as_client_b_user(
        self, client_b_user: ClientAuthorizedUser, client: AsyncClient
    ) -> None:
        await perform_status_test(client_b_user, 200, client)

    async def test_public_status_as_verified_user(
        self, verified_user: ClientAuthorizedUser, client: AsyncClient
    ) -> None:
        await perform_status_test(verified_user, 200, client)

    @pytest.mark.xfail(reason=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED)
    async def test_public_status_as_unverified_user(
        self, unverified_user: ClientAuthorizedUser, client: AsyncClient
    ) -> None:
        await perform_status_test(unverified_user, 403, client)


class TestCsrfProtection:
    async def test_get_csrf_token_as_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        response: Response = await client.get("/csrf", headers=admin_user.token_headers)
        data: dict[str, Any] = response.json()
        data_headers: Headers = response.headers
        csrf_from_data = data.get("csrf_token")
        csrf_from_header = data_headers.get(csrf_settings.csrf_header_key)

        assert 200 <= response.status_code < 300
        assert csrf_from_data is not None
        assert csrf_from_header is not None
        assert csrf_from_data == csrf_from_header

    async def test_post_csrf_token_as_admin(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        response: Response = await client.get("/csrf", headers=admin_user.token_headers)
        csrf_from_header = response.headers.get(csrf_settings.csrf_header_key)
        csrf_from_cookie = client.cookies.get(csrf_settings.csrf_name_key, "")

        assert 200 <= response.status_code < 300
        assert csrf_from_header is not None
        assert csrf_from_cookie is not None
        assert csrf_from_cookie != csrf_from_header

        resp_headers = {
            csrf_settings.csrf_header_key: csrf_from_header,
            **admin_user.token_headers,
        }
        client.cookies.set(csrf_settings.csrf_name_key, csrf_from_cookie)
        response_2: Response = await client.post("/csrf", headers=resp_headers)

        assert 200 <= response_2.status_code < 300
        assert response_2.json() is None
        assert not response_2.headers.get(csrf_settings.csrf_header_key)

    async def test_post_csrf_token_as_admin_token_missing(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        client.cookies.clear()
        response: Response = await client.post(
            "/csrf",
            headers={
                csrf_settings.csrf_header_key: get_uuid_str(),
                **admin_user.token_headers,
            },
        )
        data = response.json()

        assert response.status_code == 400
        assert data["detail"] == "Missing Cookie: `gcapi-csrf-token`."

    async def test_post_csrf_token_as_admin_error_signature_mismatch(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        response: Response = await client.get("/csrf", headers=admin_user.token_headers)
        csrf_from_header = response.headers.get(csrf_settings.csrf_header_key)
        csrf_from_cookie = client.cookies.get(csrf_settings.csrf_name_key, "")  # noqa: F841

        malformed_token = csrf_from_header + "malformed"
        response_2: Response = await client.post(
            "/csrf",
            headers={
                csrf_settings.csrf_header_key: malformed_token,
                **admin_user.token_headers,
            },
        )
        data_2 = response_2.json()

        assert response_2.status_code == 401
        assert data_2["detail"] == "The CSRF signatures submitted do not match."

    async def test_post_csrf_token_as_admin_error_bad_data(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        serializer = URLSafeTimedSerializer(
            csrf_settings.csrf_secret_key, salt="bad-salt"
        )
        token = sha1(urandom(64)).hexdigest()
        signed_token = str(serializer.dumps(token))
        resp_headers = {
            csrf_settings.csrf_header_key: token,
        }
        client.cookies.set(csrf_settings.csrf_name_key, signed_token)
        resp_headers.update(admin_user.token_headers)
        response: Response = await client.post("/csrf", headers=resp_headers)
        data_2 = response.json()

        assert response.status_code == 401
        assert data_2["detail"] == "The CSRF token is invalid."

    async def test_post_csrf_token_as_admin_invalid_headers(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        serializer = URLSafeTimedSerializer(
            csrf_settings.csrf_secret_key, salt=csrf_settings.csrf_salt
        )
        token = sha1(urandom(64)).hexdigest()
        signed_token = str(serializer.dumps(token))
        assert signed_token is not None

        response: Response = await client.post(
            "/csrf", headers={"x-csrf-bad-header": token, **admin_user.token_headers}
        )
        data_2 = response.json()

        assert response.status_code == 422
        assert data_2["detail"] == 'Bad headers. Expected "x-csrf-token" in headers'

    async def test_post_csrf_token_as_admin_invalid_header_parts(
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        admin_user: ClientAuthorizedUser,
    ) -> None:
        response: Response = await client.post(
            "/csrf",
            headers={
                "x-csrf-token": "Bearer " + get_uuid_str(),
                **admin_user.token_headers,
            },
        )
        data_2 = response.json()

        assert response.status_code == 422
        assert data_2["detail"] == 'Bad x-csrf-token header. Expected value "<Token>"'
