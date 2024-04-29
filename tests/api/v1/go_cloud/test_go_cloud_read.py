from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.go_cloud import create_random_go_cloud

from app.api.exceptions.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.crud import GoCloudPropertyRepository
from app.models import GoCloudProperty
from app.schemas import ClientRead, GoCloudPropertyRead

pytestmark = pytest.mark.asyncio


async def test_read_go_cloud_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    entry: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    response: Response = await client.get(
        f"go/cloud/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "project_name" in data
    assert "project_id" in data
    assert "project_number" in data
    assert "service_account" in data
    assert data["client_id"] == str(a_client.id)
    repo: GoCloudPropertyRepository = GoCloudPropertyRepository(db_session)
    existing_data: GoCloudProperty | None = await repo.read(entry.id)
    assert existing_data
    assert existing_data.project_name == data["project_name"]
    assert existing_data.project_id == data["project_id"]
    assert existing_data.project_number == data["project_number"]
    assert existing_data.service_account == data["service_account"]
    assert str(existing_data.client_id) == data["client_id"]


async def test_read_go_cloud_by_id_as_superuser_client_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/cloud/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.GO_CLOUD_NOT_FOUND
