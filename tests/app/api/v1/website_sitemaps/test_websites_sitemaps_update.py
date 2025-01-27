import unittest.mock
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.models.website import Website
from app.schemas import WebsiteMapRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


DUPLICATE_SITEMAP_URL = "sitemap-{}.xml".format(random_lower_string())


@pytest.mark.parametrize(
    "client_user,assign_client",
    [
        ("admin_user", False),
        ("manager_user", False),
        ("employee_user", True),
        ("client_a_user", True),
        pytest.param(
            "employee_user",
            False,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
        pytest.param(
            "client_a_user",
            False,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
        pytest.param(
            "unverified_user",
            False,
            marks=pytest.mark.xfail(reason=ErrorCode.UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_update_website_sitemap_as_user(
    client_user: Any,
    assign_client: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_client = await create_random_client(db_session)
    a_website: Website = await create_random_website(db_session, return_db_obj=True)
    a_sitemap: WebsiteMapRead = await create_random_website_map(
        db_session, a_website.id
    )
    await assign_website_to_client(db_session, a_website.id, a_client.id)
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    new_url = "{}/new-sitemap.xml".format(a_website.get_link())
    data = {"url": new_url}
    with unittest.mock.patch(
        "app.crud.website_map.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        response: Response = await client.patch(
            f"sitemaps/{a_sitemap.id}",
            headers=current_user.token_headers,
            json=data,
        )
        assert 200 <= response.status_code < 300
        entry: dict[str, Any] = response.json()
        assert entry["id"] == str(a_sitemap.id)
        assert entry["url"] == new_url
        assert entry["website_id"] == str(a_sitemap.website_id)


@pytest.mark.parametrize(
    "url_path,status_code,error_type,error_msg",
    [
        ("sitemap-{}.xml".format(random_lower_string()), 200, None, None),
        (
            None,
            400,
            "message",
            ErrorCode.ENTITY_EXISTS,
        ),
        (
            DUPLICATE_SITEMAP_URL,
            400,
            "message",
            ErrorCode.ENTITY_EXISTS,
        ),
        (
            "",
            422,
            "detail",
            f"Value error, url must be {1} characters or more",
        ),
        pytest.param(
            "sitemap-{}.xml".format(
                random_lower_string(chars=DB_STR_URLPATH_MAXLEN_INPUT + 1)
            ),
            422,
            "detail",
            f"Value error, url must be {DB_STR_URLPATH_MAXLEN_INPUT} characters or less",
        ),
    ],
)
async def test_create_website_sitemap_as_superuser_sitemap_limits(
    url_path: str | None,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website: Website = await create_random_website(db_session, return_db_obj=True)
    a_sitemap = await create_random_website_map(
        db_session, a_website.id, DUPLICATE_SITEMAP_URL
    )
    if url_path is None:
        new_url = a_sitemap.url
    else:
        new_url = url_path
    update_data: dict[str, Any] = {"url": new_url}
    with unittest.mock.patch(
        "app.crud.website_map.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        response: Response = await client.patch(
            f"sitemaps/{a_sitemap.id}",
            headers=admin_user.token_headers,
            json=update_data,
        )
        entry: dict[str, Any] = response.json()
        assert response.status_code == status_code
        if error_type == "message":
            assert error_msg in entry["detail"]
        if error_type == "detail":
            assert error_msg in entry["detail"][0]["msg"]
