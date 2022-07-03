from typing import Any, Optional

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.client import ClientsRepository
from app.db.schemas import ClientCreate
from app.db.schemas.client import ClientRead, ClientUpdate
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_client(db_session: AsyncSession) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    client_repo: ClientsRepository = ClientsRepository(session=db_session)
    client: ClientRead = await client_repo.create(
        ClientCreate(title=title, content=content)
    )
    assert client.title == title
    assert client.content == content


async def test_get_client(
    db_session: AsyncSession,
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    client_repo: ClientsRepository = ClientsRepository(session=db_session)
    client: ClientRead = await client_repo.create(
        ClientCreate(title=title, content=content)
    )
    stored_client: Optional[ClientRead] = await client_repo.read(entry_id=client.id)
    assert stored_client
    assert client.id == stored_client.id
    assert client.title == stored_client.title
    assert client.content == stored_client.content


async def test_update_client(
    db_session: AsyncSession,
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    client_repo: ClientsRepository = ClientsRepository(session=db_session)
    client: ClientRead = await client_repo.create(
        ClientCreate(title=title, content=content)
    )
    content2: str = random_lower_string()
    client2: Optional[ClientRead] = await client_repo.update(
        entry_id=client.id, schema=ClientUpdate(content=content2)
    )
    assert client is not None
    assert client2 is not None
    assert client.id == client2.id
    assert client.title == client2.title
    assert client2.content == content2


async def test_delete_client(
    db_session: AsyncSession,
) -> None:
    title: str = random_lower_string()
    content: str = random_lower_string()
    client_repo: ClientsRepository = ClientsRepository(session=db_session)
    client: ClientRead = await client_repo.create(
        ClientCreate(title=title, content=content)
    )
    client2: Any = await client_repo.delete(entry_id=client.id)
    client3: Any = await client_repo.read(entry_id=client.id)
    assert client2.id == client.id
    assert client2.title == title
    assert client2.content == content
    assert client3 is None
