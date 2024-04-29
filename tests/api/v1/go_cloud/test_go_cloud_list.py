from typing import Any, Dict

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.go_cloud import create_random_go_cloud
from tests.utils.users import get_user_by_email

from app.core.config import settings
from app.models import User
from app.schemas import ClientRead, GoCloudPropertyRead

pytestmark = pytest.mark.asyncio


async def test_list_all_sharpspring_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    entry_1: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_2: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_3: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_4: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=b_client.id
    )
    response: Response = await client.get("go/cloud/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["project_name"] == entry_1.project_name
            assert entry["project_id"] == entry_1.project_id
            assert entry["project_number"] == entry_1.project_number
            assert entry["service_account"] == entry_1.service_account
            assert entry["client_id"] == str(entry_1.client_id)
        if entry["id"] == str(entry_2.id):
            assert entry["project_name"] == entry_2.project_name
            assert entry["project_id"] == entry_2.project_id
            assert entry["project_number"] == entry_2.project_number
            assert entry["service_account"] == entry_2.service_account
            assert entry["client_id"] == str(entry_2.client_id)
        if entry["id"] == str(entry_3.id):
            assert entry["project_name"] == entry_3.project_name
            assert entry["project_id"] == entry_3.project_id
            assert entry["project_number"] == entry_3.project_number
            assert entry["service_account"] == entry_3.service_account
            assert entry["client_id"] == str(entry_3.client_id)
        if entry["id"] == str(entry_4.id):
            assert entry["project_name"] == entry_4.project_name
            assert entry["project_id"] == entry_4.project_id
            assert entry["project_number"] == entry_4.project_number
            assert entry["service_account"] == entry_4.service_account
            assert entry["client_id"] == str(entry_4.client_id)


async def test_list_all_sharpspring_as_superuser_query_client_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    entry_1: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_2: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_3: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_4: GoCloudPropertyRead = await create_random_go_cloud(  # noqa: F841
        db_session, client_id=b_client.id
    )
    entry_5: GoCloudPropertyRead = await create_random_go_cloud(  # noqa: F841
        db_session, client_id=b_client.id
    )
    response: Response = await client.get(
        "go/cloud/",
        headers=admin_token_headers,
        params=QueryParams(client_id=a_client.id),
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 3
    assert data["size"] == 1000
    assert len(data["results"]) == 3
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["project_name"] == entry_1.project_name
            assert entry["project_id"] == entry_1.project_id
            assert entry["project_number"] == entry_1.project_number
            assert entry["service_account"] == entry_1.service_account
            assert entry["client_id"] == str(entry_1.client_id)
        if entry["id"] == str(entry_2.id):
            assert entry["project_name"] == entry_2.project_name
            assert entry["project_id"] == entry_2.project_id
            assert entry["project_number"] == entry_2.project_number
            assert entry["service_account"] == entry_2.service_account
            assert entry["client_id"] == str(entry_2.client_id)
        if entry["id"] == str(entry_3.id):
            assert entry["project_name"] == entry_3.project_name
            assert entry["project_id"] == entry_3.project_id
            assert entry["project_number"] == entry_3.project_number
            assert entry["service_account"] == entry_3.service_account
            assert entry["client_id"] == str(entry_3.client_id)


async def test_list_all_sharpspring_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_user_a_client = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    entry_1: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_2: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_3: GoCloudPropertyRead = await create_random_go_cloud(
        db_session, client_id=a_client.id
    )
    entry_4: GoCloudPropertyRead = await create_random_go_cloud(  # noqa: F841
        db_session, client_id=b_client.id
    )
    response: Response = await client.get("go/cloud/", headers=employee_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 3
    assert data["size"] == 1000
    assert len(data["results"]) == 3
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["project_name"] == entry_1.project_name
            assert entry["project_id"] == entry_1.project_id
            assert entry["project_number"] == entry_1.project_number
            assert entry["service_account"] == entry_1.service_account
            assert entry["client_id"] == str(entry_1.client_id)
        if entry["id"] == str(entry_2.id):
            assert entry["project_name"] == entry_2.project_name
            assert entry["project_id"] == entry_2.project_id
            assert entry["project_number"] == entry_2.project_number
            assert entry["service_account"] == entry_2.service_account
            assert entry["client_id"] == str(entry_2.client_id)
        if entry["id"] == str(entry_3.id):
            assert entry["project_name"] == entry_3.project_name
            assert entry["project_id"] == entry_3.project_id
            assert entry["project_number"] == entry_3.project_number
            assert entry["service_account"] == entry_3.service_account
            assert entry["client_id"] == str(entry_3.client_id)
