from typing import Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client

from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_list_all_clients_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_1: ClientRead = await create_random_client(db_session)
    entry_2: ClientRead = await create_random_client(db_session)
    response: Response = await client.get("clients/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 8
    assert data["size"] == 1000
    assert len(data["results"]) == 8
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert entry["description"] == entry_1.description
            assert entry["is_active"] == entry_1.is_active
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["description"] == entry_2.description
            assert entry["is_active"] == entry_2.is_active


async def test_list_all_clients_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get("clients/", headers=employee_token_headers)
    assert 200 <= response.status_code < 300
    data = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == 1
    assert data["size"] == 1000
    assert len(data["results"]) == 1
