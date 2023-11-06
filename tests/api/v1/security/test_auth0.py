from typing import Any, Dict

from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession


async def test_auth0_bearer_token_missing(
    client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    response: Response = await client.get(
        "/users/me",
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Missing bearer token"
