from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.models import User
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_create_go_cloud_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["project_name"] == project_name
    assert entry["project_id"] == project_id
    assert entry["project_number"] == project_number
    assert entry["service_account"] == service_account
    assert entry["client_id"] == str(a_client.id)


async def test_create_go_cloud_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_client_id = get_uuid_str()
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": fake_client_id,
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_create_go_cloud_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_user_a_client = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["project_name"] == project_name
    assert entry["project_id"] == project_id
    assert entry["project_number"] == project_number
    assert entry["service_account"] == service_account
    assert entry["client_id"] == str(a_client.id)


async def test_create_go_cloud_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_create_go_cloud_as_superuser_go_cloud_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert entry["project_name"] == project_name
    assert entry["project_id"] == project_id
    assert entry["project_number"] == project_number
    assert entry["service_account"] == service_account
    assert entry["client_id"] == str(a_client.id)
    project_id_2: str = random_lower_string()
    project_number_2: str = random_lower_string()
    service_account_2: str = random_lower_string()
    data_in_2: Dict[str, Any] = {
        "project_name": entry["project_name"],
        "project_id": project_id_2,
        "project_number": project_number_2,
        "service_account": service_account_2,
        "client_id": str(a_client.id),
    }
    response_2: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.GO_CLOUD_EXISTS


async def test_create_go_cloud_as_superuser_go_cloud_project_name_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = ""
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, project_name is required"


async def test_create_go_cloud_as_superuser_go_cloud_project_name_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, project_name must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_create_go_cloud_as_superuser_go_cloud_project_id_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = ""
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, project_id is required"


async def test_create_go_cloud_as_superuser_go_cloud_project_id_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = "a" * (DB_STR_64BIT_MAXLEN_INPUT + 1)
    project_number: str = random_lower_string()
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, project_id must be {DB_STR_64BIT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_create_go_cloud_as_superuser_go_cloud_project_number_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = ""
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "Value error, project_number is required"


async def test_create_go_cloud_as_superuser_go_cloud_project_number_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = "a" * (DB_STR_64BIT_MAXLEN_INPUT + 1)
    service_account: str = random_lower_string()
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, project_number must be {DB_STR_64BIT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_create_go_cloud_as_superuser_go_cloud_service_account_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = "a"
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, service_account must be {5} characters or more"
    )


async def test_create_go_cloud_as_superuser_go_cloud_service_account_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    project_name: str = random_lower_string()
    project_id: str = random_lower_string()
    project_number: str = random_lower_string()
    service_account: str = "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data_in: Dict[str, Any] = {
        "project_name": project_name,
        "project_id": project_id,
        "project_number": project_number,
        "service_account": service_account,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        "go/cloud/",
        headers=admin_token_headers,
        json=data_in,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert (
        entry["detail"][0]["msg"]
        == f"Value error, service_account must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )
