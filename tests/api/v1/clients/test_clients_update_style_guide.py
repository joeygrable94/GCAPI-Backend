from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    create_random_client,
    create_random_client_style_guide,
)
from tests.utils.users import get_user_by_email

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.models.user import User
from app.models.user_client import UserClient
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_update_client_style_guide_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_a: ClientRead = await create_random_client(db_session)
    style_guide = create_random_client_style_guide()
    data: Dict[str, str] = {"style_guide": style_guide}
    response: Response = await client.patch(
        f"clients/{entry_a.id}/style-guide",
        headers=admin_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["id"] == str(entry_a.id)
    assert updated_entry["title"] == str(entry_a.title)
    assert updated_entry["style_guide"] == style_guide
    assert "is_active" not in updated_entry
    assert "description" not in updated_entry


async def test_update_client_style_guide_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_employee
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    style_guide = create_random_client_style_guide()
    data: Dict[str, str] = {"style_guide": style_guide}
    response: Response = await client.patch(
        f"clients/{a_client.id}/style-guide",
        headers=employee_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["id"] == str(a_client.id)
    assert updated_entry["title"] == str(a_client.title)
    assert updated_entry["style_guide"] == style_guide
    assert "is_active" not in updated_entry
    assert "description" not in updated_entry


async def test_update_client_style_guide_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    style_guide = create_random_client_style_guide()
    data: Dict[str, str] = {"style_guide": style_guide}
    response: Response = await client.patch(
        f"clients/{a_client.id}/style-guide",
        headers=employee_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert updated_entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_update_client_style_guide_as_client(
    client: AsyncClient,
    db_session: AsyncSession,
    client_a_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_client_a
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    style_guide = create_random_client_style_guide()
    data: Dict[str, str] = {"style_guide": style_guide}
    response: Response = await client.patch(
        f"clients/{a_client.id}/style-guide",
        headers=client_a_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["id"] == str(a_client.id)
    assert updated_entry["title"] == str(a_client.title)
    assert updated_entry["style_guide"] == style_guide
    assert "is_active" not in updated_entry
    assert "description" not in updated_entry


async def test_update_client_style_guide_as_client_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    client_a_token_headers: Dict[str, str],
) -> None:
    b_user: User = await get_user_by_email(
        db_session=db_session, email=settings.auth.first_client_b
    )
    b_client: ClientRead = await create_random_client(db_session)
    a_user_client: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, b_user, b_client
    )
    style_guide = create_random_client_style_guide()
    data: Dict[str, str] = {"style_guide": style_guide}
    response: Response = await client.patch(
        f"clients/{b_client.id}/style-guide",
        headers=client_a_token_headers,
        json=data,
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert updated_entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS
