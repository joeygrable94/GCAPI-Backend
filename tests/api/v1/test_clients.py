from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.utils import random_lower_string

from app.api.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.db.repositories import ClientsRepository
from app.db.schemas import ClientRead, ClientUpdate

pytestmark = pytest.mark.asyncio


async def test_list_clients_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_1: ClientRead = await create_random_client(db_session)
    entry_2: ClientRead = await create_random_client(db_session)
    response: Response = await client.get("clients/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_entries: Any = response.json()
    assert len(all_entries) > 1
    for entry in all_entries:
        assert "title" in entry
        assert "content" in entry
        if entry["title"] == entry_1.title:
            assert entry["title"] == entry_1.title
            assert entry["content"] == entry_1.content
        if entry["title"] == entry_2.title:
            assert entry["title"] == entry_2.title
            assert entry["content"] == entry_2.content


async def test_list_clients_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    testuser_token_headers: Dict[str, str],
) -> None:
    entry_1: ClientRead = await create_random_client(db_session)  # noqa: F841
    entry_2: ClientRead = await create_random_client(db_session)  # noqa: F841
    response: Response = await client.get("clients/", headers=testuser_token_headers)
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_create_client_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["title"] == title
    assert entry["content"] == content


async def test_create_client_as_superuser_client_already_exists(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["title"] == title
    assert entry["content"] == content
    content_2: str = random_lower_string()
    data_2: Dict[str, str] = {"title": title, "content": content_2}
    response_2: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == "Client exists"


async def test_create_client_as_testuser(
    client: AsyncClient,
    testuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=testuser_token_headers,
        json=data,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_create_client_as_superuser_client_title_too_short(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = "1234"
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "title must contain 5 or more characters"


async def test_create_client_as_superuser_client_title_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string() * 4
    content: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "title must contain less than 96 characters"


async def test_create_client_as_superuser_client_content_too_long(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string() * 10
    data: Dict[str, str] = {"title": title, "content": content}
    response: Response = await client.post(
        "clients/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 422
    entry: Dict[str, Any] = response.json()
    assert entry["detail"][0]["msg"] == "content must contain less than 255 characters"


async def test_read_client_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.get(
        f"clients/{entry.id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    repo: ClientsRepository = ClientsRepository(db_session)
    existing_data: Any = await repo.read_by("title", entry.title)
    assert existing_data
    assert existing_data.title == data["title"]


async def test_read_client_by_id_as_superuser_client_not_found(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"clients/{entry_id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Client not found"


async def test_read_client_by_id_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    testuser_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.get(
        f"clients/{entry.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_update_client_as_superuser_title_too_short(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    title: str = "1234"
    data: Dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"] == "title must contain 5 or more characters"
    )


async def test_update_client_as_superuser_title_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    title: str = random_lower_string() * 4
    data: Dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "title must contain less than 96 characters"
    )


async def test_update_client_as_superuser_content_too_long(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    content: str = random_lower_string() * 10
    data: Dict[str, str] = {"content": content}
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert (
        updated_entry["detail"][0]["msg"]
        == "content must contain less than 255 characters"
    )


async def test_update_client_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    entry_b: ClientRead = await create_random_client(db_session)
    update_dict = ClientUpdate(
        title=entry_b.title,
        content="New Content",
    )
    response: Response = await client.patch(
        f"clients/{entry_a.id}",
        headers=superuser_token_headers,
        json=update_dict.dict(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == "Client exists"


async def test_delete_client_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.delete(
        f"clients/{entry.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    repo: ClientsRepository = ClientsRepository(db_session)
    data_not_found: Optional[Any] = await repo.read_by("title", entry.title)
    assert data_not_found is None


async def test_delete_client_by_id_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    testuser_token_headers: Dict[str, str],
) -> None:
    entry: ClientRead = await create_random_client(db_session)
    response: Response = await client.delete(
        f"clients/{entry.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS
