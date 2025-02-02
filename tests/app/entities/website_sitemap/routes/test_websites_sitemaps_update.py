import unittest.mock
from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
)
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.website_sitemap.constants import ERROR_MESSAGE_XML_INVALID
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
)
from app.utilities.uuids import get_uuid_str
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
    "client_user,assign_client,status_code",
    [
        ("admin_user", False, 200),
        ("manager_user", False, 200),
        ("employee_user", True, 200),
        ("client_a_user", True, 200),
        pytest.param(
            "employee_user",
            False,
            405,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
        pytest.param(
            "client_a_user",
            False,
            405,
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
        pytest.param(
            "unverified_user",
            False,
            403,
            marks=pytest.mark.xfail(reason=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_update_website_sitemap_as_user(
    client_user: Any,
    assign_client: bool,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session, return_db_obj=True)
    a_sitemap = await create_random_website_map(db_session, a_website.id)
    await assign_website_to_client(db_session, a_website.id, a_client.id)
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    new_url = "{}/new-sitemap.xml".format(a_website.get_link())
    data = {"url": new_url}
    with unittest.mock.patch(
        "app.entities.website_sitemap.crud.WebsiteMapRepository.is_sitemap_url_xml_valid"
    ) as mock_valid_sitemap_xml:
        mock_valid_sitemap_xml.return_value = True
        response: Response = await client.patch(
            f"sitemaps/{a_sitemap.id}",
            headers=current_user.token_headers,
            json=data,
        )
        assert response.status_code == status_code
        if status_code == 200:
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
            ERROR_MESSAGE_ENTITY_EXISTS,
        ),
        (
            DUPLICATE_SITEMAP_URL,
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
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
async def test_update_website_sitemap_as_superuser_sitemap_limits(
    url_path: str | None,
    status_code: int,
    error_type: str,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session, return_db_obj=True)
    a_sitemap = await create_random_website_map(
        db_session, a_website.id, DUPLICATE_SITEMAP_URL
    )
    if url_path is None:
        new_url = a_sitemap.url
    else:
        new_url = url_path
    update_data: dict[str, Any] = {"url": new_url}
    with unittest.mock.patch(
        "app.entities.website_sitemap.crud.WebsiteMapRepository.is_sitemap_url_xml_valid"
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


async def test_update_website_sitemap_as_superuser_url_xml_invalid(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session, domain="getcommunity.com")
    a_sitemap = await create_random_website_map(db_session, website_id=a_website.id)
    data = {
        "url": "sitemap-invalid.xml",
        "website_id": str(a_website.id),
    }
    response: Response = await client.patch(
        f"sitemaps/{a_sitemap.id}",
        headers=admin_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 422
    assert entry["detail"] == ERROR_MESSAGE_XML_INVALID


async def test_update_website_sitemap_as_superuser_url_invalid_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    bad_website_id = get_uuid_str()
    a_sitemap = await create_random_website_map(
        db_session, website_id=bad_website_id, url_path="sitemap.xml"
    )
    data = {
        "url": "sitemap_index.xml",
        "is_active": not a_sitemap.is_active,
    }
    response: Response = await client.patch(
        f"sitemaps/{a_sitemap.id}",
        headers=admin_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in entry["detail"]
