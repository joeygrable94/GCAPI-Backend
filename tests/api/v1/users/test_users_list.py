# from typing import Any, Dict, List
from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import PagedResponseSchema

# from app.schemas import UserRead, ClientRead
from app.schemas.user import UserReadAsAdmin

# from tests.utils.clients import create_random_client


pytestmark = pytest.mark.asyncio


async def test_list_users_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get(
        "users/",
        headers=admin_token_headers,
    )
    data: PagedResponseSchema[UserReadAsAdmin] = PagedResponseSchema(**response.json())
    assert 200 <= response.status_code < 300
    assert data.page == 1
    assert data.total == 1
    assert data.size == 100
    assert len(data.results) > 0


async def test_list_users_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get(
        "users/",
        headers=employee_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert data["detail"] == "You do not have permission to access this resource"
    assert response.status_code == 405
