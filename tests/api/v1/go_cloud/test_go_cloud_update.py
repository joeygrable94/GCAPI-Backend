from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.go_cloud import create_random_go_cloud
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.utilities import get_uuid_str
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.schemas import ClientRead, GoCloudPropertyRead

pytestmark = pytest.mark.asyncio


async def test_update_go_cloud_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    project_name: str = random_lower_string(64)
    data: Dict[str, str] = {"project_name": project_name}
    response: Response = await client.patch(
        f"go/cloud/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["id"] == str(entry_a.id)
    assert updated_entry["project_name"] == project_name
    assert updated_entry["project_id"] == entry_a.project_id
    assert updated_entry["project_number"] == entry_a.project_number
    assert updated_entry["service_account"] == entry_a.service_account
    assert updated_entry["client_id"] == str(a_client.id)


async def test_update_go_cloud_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    fake_client_id = get_uuid_str()
    project_name: str = random_lower_string(64)
    data: Dict[str, str] = {"project_name": project_name, "client_id": fake_client_id}
    response: Response = await client.patch(
        f"go/cloud/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert updated_entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_update_go_cloud_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_b: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    update_data: Dict[str, str] = {
        "project_name": entry_b.project_name,
    }
    response: Response = await client.patch(
        f"go/cloud/{entry_a.id}",
        headers=admin_token_headers,
        json=update_data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == ErrorCode.GO_CLOUD_EXISTS


async def test_update_go_cloud_as_superuser_project_name_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    project_name: str = ""
    data: Dict[str, str] = {"project_name": project_name}
    response: Response = await client.patch(
        f"go/cloud/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert updated_entry["detail"][0]["msg"] == "Value error, project_name is required"


async def test_update_go_cloud_as_superuser_project_name_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    project_name: str = random_lower_string(1) * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data: Dict[str, str] = {"project_name": project_name}
    response: Response = await client.patch(
        f"go/cloud/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, project_name must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_update_go_cloud_as_superuser_service_account_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    service_account: str = "a"
    data: Dict[str, str] = {"service_account": service_account}
    response: Response = await client.patch(
        f"go/cloud/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, service_account must be {5} characters or more"
    )


async def test_update_go_cloud_as_superuser_service_account_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    service_account: str = random_lower_string(1) * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
    data: Dict[str, str] = {"service_account": service_account}
    response: Response = await client.patch(
        f"go/cloud/{entry_a.id}",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == f"Value error, service_account must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less"  # noqa: E501
    )


async def test_update_go_cloud_as_superuser_service_account_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry_a: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id, is_service_account=True
    )
    entry_b: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id, is_service_account=True
    )
    update_data: Dict[str, str | None] = {
        "service_account": entry_b.service_account,
    }
    response: Response = await client.patch(
        f"go/cloud/{entry_a.id}",
        headers=admin_token_headers,
        json=update_data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == ErrorCode.GO_CLOUD_EXISTS
