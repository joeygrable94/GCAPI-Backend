"""
from time import sleep
from typing import Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


async def test_limiter(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    response = await client.get("/status", headers=admin_token_headers)
    assert response.status_code == 200
    sleep(6)

    response = await client.get("/status", headers=admin_token_headers)
    assert response.status_code == 200

    response = await client.get("/status", headers=admin_token_headers)
    assert response.status_code == 429
    sleep(6)

    response = await client.get("/status", headers=admin_token_headers)
    assert response.status_code == 200

    response = await client.get("/status", headers=admin_token_headers)
    assert response.status_code == 429
    sleep(6)

    response = await client.get("/status", headers=admin_token_headers)
    assert response.status_code == 200

    response = await client.get("/status", headers=admin_token_headers)
    assert response.status_code == 429
    sleep(6)


async def test_limiter_multiple(
    client: AsyncClient, admin_token_headers: Dict[str, str]
) -> None:
    response = await client.get("/rate-limited-multiple", headers=admin_token_headers)
    assert response.status_code == 200

    response = await client.get("/rate-limited-multiple", headers=admin_token_headers)
    assert response.status_code == 429
    sleep(6)

    response = await client.get("/rate-limited-multiple", headers=admin_token_headers)
    assert response.status_code == 200

    response = await client.get("/rate-limited-multiple", headers=admin_token_headers)
    assert response.status_code == 429
    sleep(16)

    response = await client.get("/rate-limited-multiple", headers=admin_token_headers)
    assert response.status_code == 200
    sleep(6)


async def test_limiter_websockets(
    client: AsyncClient,
    admin_token_headers: Dict[str, str],
):
    async with client.stream("GET", "/rate-limited-websocket") as ws:
        await ws.send_text("Hi")
        data = await ws.receive_text()
        assert data == "Hello, world"

        ws.send_text("Hi")
        data = ws.receive_text()
        assert data == "Hello again"

        ws.send_text("Hi 2")
        data = ws.receive_text()
        assert data == "Hello, world"
        ws.close()
"""
