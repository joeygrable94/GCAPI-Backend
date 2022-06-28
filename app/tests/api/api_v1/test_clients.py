from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user import UsersRepository
from app.db.schemas.client import ClientRead
from app.tests.utils.client import create_random_client
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_client(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    data: Dict[str, str] = {"title": "Testing", "content": "One. Two.. Three..."}
    response: Response = await client.post(
        "clients/", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    content: Dict[str, Any] = response.json()
    assert content["title"] == data["title"]
    assert content["content"] == data["content"]
    assert "id" in content


async def test_read_client(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    gcclient: ClientRead = await create_random_client(db_session, user_repo)
    response: Response = await client.get(
        f"clients/{gcclient.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    content: Dict[str, Any] = response.json()
    assert content["title"] == gcclient.title
    assert content["content"] == gcclient.content
    assert content["id"] == str(gcclient.id)


async def test_update_client(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    gcclient: ClientRead = await create_random_client(db_session, user_repo)
    new_title: str = random_lower_string()
    new_content: str = random_lower_string()
    data: Dict[str, str] = {"title": new_title, "content": new_content}
    response: Response = await client.patch(
        f"clients/{gcclient.id}", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    content: Dict[str, Any] = response.json()
    assert content["title"] != gcclient.title
    assert content["title"] == new_title
    assert content["content"] != gcclient.content
    assert content["content"] == new_content
    assert content["id"] == str(gcclient.id)


async def test_delete_client(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    gcclient: ClientRead = await create_random_client(db_session, user_repo)
    response: Response = await client.delete(
        f"clients/{gcclient.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content: Dict[str, Any] = response.json()
    assert content["title"] == gcclient.title
    assert content["content"] == gcclient.content
    assert content["id"] == str(gcclient.id)


async def test_list_clients(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    user_repo: UsersRepository = UsersRepository(session=db_session)
    client_1: ClientRead = await create_random_client(  # noqa: F841
        db_session, user_repo
    )
    client_2: ClientRead = await create_random_client(  # noqa: F841
        db_session, user_repo
    )
    client_3: ClientRead = await create_random_client(  # noqa: F841
        db_session, user_repo
    )
    response: Response = await client.get("clients/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_clients: Dict[str, Any] = response.json()
    assert len(all_clients) > 1
    for api_client in all_clients:
        assert "id" in api_client
        assert "title" in api_client
        assert "content" in api_client
