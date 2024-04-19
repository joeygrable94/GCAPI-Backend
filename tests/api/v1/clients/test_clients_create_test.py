"""

from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_client_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    title: str = random_lower_string()
    description: str = random_lower_string()
    data: Dict[str, str] = {"title": title, "description": description}
    response: Response = await client.post(
        "clients/",
        headers=admin_token_headers,
        json=data,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == title
    assert entry["description"] == description
    assert False

"""
