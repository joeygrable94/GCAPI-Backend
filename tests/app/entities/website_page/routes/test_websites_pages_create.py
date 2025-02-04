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
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.organizations import (
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


DUPLICATE_URL = "/%s/%s/" % (random_lower_string(16), random_lower_string(16))


@pytest.mark.parametrize(
    "client_user,assign_organization,status_code",
    [
        ("admin_user", True, 200),
        ("manager_user", True, 200),
        ("employee_user", True, 200),
        ("client_a_user", True, 200),
        ("client_b_user", True, 200),
        ("verified_user", True, 200),
        pytest.param(
            "unverified_user",
            False,
            400,
            marks=pytest.mark.xfail(reason=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_create_website_page_as_user(
    client_user: Any,
    assign_organization: bool,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    data = {
        "url": "/",
        "status": 200,
        "priority": 0.5,
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        "webpages/",
        headers=current_user.token_headers,
        json=data,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        assert entry["url"] == "/"
        assert entry["status"] == 200
        assert entry["priority"] == 0.5
        assert entry["website_id"] == str(a_website.id)


@pytest.mark.parametrize(
    "url,status,priority,fake_website,status_code,error_type,error_msg",
    [
        ("/" + random_lower_string(), 200, 0.5, False, 200, None, None),
        (
            DUPLICATE_URL,
            200,
            0.5,
            False,
            400,
            "message",
            ERROR_MESSAGE_ENTITY_EXISTS,
        ),
        ("", 200, 0.5, False, 422, "detail", "Value error, url is required"),
        (
            "/" + "a" * DB_STR_URLPATH_MAXLEN_INPUT,
            200,
            0.5,
            False,
            422,
            "detail",
            f"Value error, url must be {DB_STR_URLPATH_MAXLEN_INPUT} characters or less",
        ),
        (
            "/" + random_lower_string(),
            200,
            0.5,
            True,
            404,
            "message",
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
        ),
    ],
)
async def test_create_website_page_as_superuser_website_limits(
    url: str,
    status: int,
    priority: float,
    fake_website: bool,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_website = await create_random_website(db_session)
    await create_random_website_page(db_session, a_website.id, path=DUPLICATE_URL)
    data = {
        "url": url,
        "status": status,
        "priority": priority,
    }
    if fake_website:
        data["website_id"] = get_uuid_str()
    else:
        data["website_id"] = str(a_website.id)
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
