# from typing import Any, Dict, List
from typing import Dict, List

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

# from app.schemas import UserRead, ClientRead
from app.schemas import UserRead

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
    data: List[UserRead] = [UserRead.model_validate(v) for v in response.json()]
    assert 200 <= response.status_code < 300
    assert len(data) > 0


"""
async def test_list_users_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    client_in_db: ClientRead = await create_random_client(db_session)
    response: Response = await client.get(
        f"users/?client_id={client_in_db.id}",
        headers=employee_token_headers,
    )
    data: Dict[str, Any] = response.json()
    print(data)
    assert False
    assert data["detail"] == 'Insufficient permissions'
    assert response.status_code == 403
"""
