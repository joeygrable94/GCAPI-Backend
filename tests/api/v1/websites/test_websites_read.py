from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_boolean
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.schemas import WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_read_website_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    domain: str = "greatersmc.com"
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=admin_token_headers,
        json=data,
    )
    new_website: Dict[str, Any] = response.json()
    entry = WebsiteRead(**new_website["website"])
    response: Response = await client.get(
        f"websites/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)


async def test_read_website_by_id_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    # get empoyee user
    an_employee = await get_user_by_email(db_session, settings.auth.first_employee)
    # create a website
    a_website = await create_random_website(db_session)
    # create a client
    a_client = await create_random_client(db_session)
    # associate the website with a client
    a_client_website = await assign_website_to_client(  # noqa: F841
        db_session, a_website, a_client
    )
    # associate the user with a client
    a_user_client = await assign_user_to_client(  # noqa: F841
        db_session, an_employee, a_client
    )
    # check if the user can read the website
    response: Response = await client.get(
        f"websites/{a_website.id}",
        headers=employee_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(a_website.id)


async def test_read_website_by_id_as_superuser_website_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"websites/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.WEBSITE_NOT_FOUND
