from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.go_sc import create_random_go_search_console_property
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.models import User, Website
from app.schemas import ClientRead, GoSearchConsolePropertyRead, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_update_go_sc_property_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_go_sc: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, a_client.id, a_website.id
        )
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["website_id"] == str(a_website.id)
    assert entry["client_id"] == str(a_client.id)


async def test_update_go_sc_property_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_go_sc: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, a_client.id, a_website.id
        )
    )
    data_in: Dict[str, Any] = dict(
        client_id=get_uuid_str(),
    )
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_update_go_sc_property_as_superuser_website_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_go_sc: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, a_client.id, a_website.id
        )
    )
    data_in: Dict[str, Any] = dict(
        website_id=get_uuid_str(),
    )
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.WEBSITE_NOT_FOUND


async def test_update_go_sc_property_as_superuser_title_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    b_website: Website | WebsiteRead = await create_random_website(db_session)
    a_go_sc: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, a_client.id, a_website.id
        )
    )
    b_go_sc: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, a_client.id, b_website.id
        )
    )
    data_in: Dict[str, Any] = dict(title=b_go_sc.title)
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert entry["detail"] == ErrorCode.GO_SEARCH_PROPERTY_EXISTS


async def test_update_go_sc_property_as_superuser_go_sc_property_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    b_website: Website | WebsiteRead = await create_random_website(db_session)
    c_website: Website | WebsiteRead = await create_random_website(db_session)
    a_go_sc: GoSearchConsolePropertyRead
    b_go_sc: GoSearchConsolePropertyRead  # noqa: F841
    c_go_sc: GoSearchConsolePropertyRead  # noqa: F841
    a_go_sc = await create_random_go_search_console_property(
        db_session, a_client.id, a_website.id
    )
    b_go_sc = await create_random_go_search_console_property(  # noqa: F841
        db_session, a_client.id, b_website.id
    )
    c_go_sc = await create_random_go_search_console_property(  # noqa: F841
        db_session, a_client.id, c_website.id
    )
    data_in: Dict[str, Any] = dict(
        client_id=str(a_client.id),
        website_id=str(b_website.id),
    )
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert entry["detail"] == ErrorCode.GO_SEARCH_PROPERTY_EXISTS


async def test_update_go_sc_property_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    await assign_user_to_client(db_session, a_user, a_client)
    await assign_website_to_client(db_session, a_website, a_client)
    a_go_sc = await create_random_go_search_console_property(
        db_session, a_client.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["website_id"] == str(a_website.id)
    assert entry["client_id"] == str(a_client.id)


async def test_update_go_sc_property_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(  # noqa: F841
        db_session, settings.auth.first_employee
    )
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_go_sc = await create_random_go_search_console_property(
        db_session, a_client.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_update_go_sc_property_as_employee_forbidden_client_access(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    b_website: Website | WebsiteRead = await create_random_website(db_session)
    await assign_user_to_client(db_session, a_user, a_client)
    await assign_website_to_client(db_session, a_website, a_client)
    await assign_website_to_client(db_session, b_website, a_client)
    a_go_sc = await create_random_go_search_console_property(
        db_session, a_client.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        client_id=str(b_client.id),
    )
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_update_go_sc_property_as_employee_forbidden_website_access(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    b_website: Website | WebsiteRead = await create_random_website(db_session)
    await assign_user_to_client(db_session, a_user, a_client)
    await assign_website_to_client(db_session, a_website, a_client)
    await assign_website_to_client(db_session, b_website, b_client)
    a_go_sc = await create_random_go_search_console_property(
        db_session, a_client.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        website_id=str(b_website.id),
    )
    response: Response = await client.patch(
        f"go/search/property/{a_go_sc.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS
