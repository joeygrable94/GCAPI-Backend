from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.db.constants import DB_STR_URLPATH_MAXLEN_INPUT
from app.models.website import Website
from app.schemas.client import ClientRead
from app.schemas.website import WebsiteRead
from app.schemas.website_map import WebsiteMapRead
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.website_maps import create_random_website_map
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


DUPLICATE_URL = "/%s/%s/" % (random_lower_string(16), random_lower_string(16))


@pytest.mark.parametrize(
    "client_user,assign_client",
    [
        ("admin_user", True),
        ("manager_user", True),
        ("employee_user", True),
        ("client_a_user", True),
        ("client_b_user", True),
        ("verified_user", True),
        pytest.param(
            "unverified_user",
            False,
            marks=pytest.mark.xfail(reason=ErrorCode.UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_create_website_page_as_user(
    client_user: Any,
    assign_client: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_sitemap: WebsiteMapRead = await create_random_website_map(
        db_session, a_website.id
    )
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
        await assign_website_to_client(db_session, a_website.id, a_client.id)
    data = {
        "url": "/",
        "status": 200,
        "priority": 0.5,
        "website_id": str(a_website.id),
        "sitemap_id": str(a_sitemap.id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=current_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["url"] == "/"
    assert entry["status"] == 200
    assert entry["priority"] == 0.5
    assert entry["website_id"] == str(a_website.id)
    assert entry["sitemap_id"] == str(a_sitemap.id)


@pytest.mark.parametrize(
    "url,status,priority,fake_website,assign_sitemap,status_code,error_type,error_msg",
    [
        ("/" + random_lower_string(), 200, 0.5, False, False, 200, None, None),
        ("/" + random_lower_string(), 200, 0.5, False, True, 200, None, None),
        (
            "/" + random_lower_string(),
            200,
            0.5,
            False,
            None,
            400,
            "message",
            ErrorCode.ENTITY_RELATIONSHOP_NOT_FOUND,
        ),
        (
            DUPLICATE_URL,
            200,
            0.5,
            False,
            None,
            400,
            "message",
            ErrorCode.ENTITY_EXISTS,
        ),
        ("", 200, 0.5, False, True, 422, "detail", "Value error, url is required"),
        (
            "/" + "a" * DB_STR_URLPATH_MAXLEN_INPUT,
            200,
            0.5,
            False,
            True,
            422,
            "detail",
            f"Value error, url must be {DB_STR_URLPATH_MAXLEN_INPUT} characters or less",
        ),
        (
            "/" + random_lower_string(),
            200,
            0.5,
            True,
            True,
            404,
            "message",
            ErrorCode.ENTITY_NOT_FOUND,
        ),
    ],
)
async def test_create_website_page_as_superuser_website_limits(
    url: str,
    status: int,
    priority: float,
    fake_website: bool,
    assign_sitemap: bool | None,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_sitemap = await create_random_website_map(db_session, a_website.id)
    await create_random_website_page(
        db_session, a_website.id, a_sitemap.id, path=DUPLICATE_URL
    )
    data = {
        "url": url,
        "status": status,
        "priority": priority,
    }
    if fake_website:
        data["website_id"] = get_uuid_str()
    else:
        data["website_id"] = str(a_website.id)
    if assign_sitemap is None:
        fake_sitemap_id = get_uuid_str()
        data["sitemap_id"] = fake_sitemap_id
    elif assign_sitemap:
        data["sitemap_id"] = str(a_sitemap.id)
    response: Response = await client.post(
        "webpages/",
        headers=admin_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]
