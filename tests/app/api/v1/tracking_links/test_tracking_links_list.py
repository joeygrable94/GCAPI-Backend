from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.tracking_link import create_random_tracking_link
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,link_count,query_client,assign_user",
    [
        ("admin_user", 3, False, False),
        ("manager_user", 3, False, False),
        ("employee_user", 2, False, True),
        ("admin_user", 1, True, False),
        ("manager_user", 1, True, False),
        ("employee_user", 0, False, False),
    ],
)
async def test_list_all_tracking_link_as_user(
    client_user: Any,
    link_count: int,
    query_client: bool,
    assign_user: bool,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user: User = await get_user_by_email(db_session, current_user.email)
    client_a = await create_random_client(db_session)
    client_b = await create_random_client(db_session)
    await create_random_tracking_link(db_session, client_a.id)
    await create_random_tracking_link(db_session, client_a.id)
    await create_random_tracking_link(db_session, client_b.id)
    if not this_user.is_superuser and assign_user:
        await assign_user_to_client(db_session, this_user.id, client_a.id)
    if query_client:
        response: Response = await client.get(
            "utmlinks/",
            params={"client_id": str(client_b.id)},
            headers=current_user.token_headers,
        )
    else:
        response: Response = await client.get(
            "utmlinks/", headers=current_user.token_headers
        )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert data["page"] == 1
    assert data["total"] == link_count
    assert data["size"] == 1000
    assert len(data["results"]) == link_count


@pytest.mark.parametrize(
    "client_user, link_count, q_client, q_scheme, q_domain, q_destination, q_url_path, q_campaign, q_medium, q_source, q_content, q_term, q_active",
    [
        (
            "admin_user",
            13,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            2,
            True,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            "http",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            12,
            None,
            "https",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            "example.com",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            None,
            "https://another.com/destination",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            None,
            None,
            "/example-path",
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            None,
            None,
            None,
            "campaign-name",
            None,
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            None,
            None,
            None,
            None,
            "medium-name",
            None,
            None,
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "source-name",
            None,
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "content-name",
            None,
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "term-name",
            None,
        ),
        (
            "admin_user",
            1,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            True,
        ),
    ],
    ids=[
        "admin user query all links",
        "admin user query all links by client_id",
        "admin user query all links by scheme http",
        "admin user query all links by scheme https",
        "admin user query all links by domain",
        "admin user query all links by destination",
        "admin user query all links by url_path",
        "admin user query all links by utm_campaign",
        "admin user query all links by utm_medium",
        "admin user query all links by utm_source",
        "admin user query all links by utm_content",
        "admin user query all links by utm_term",
        "admin user query all links by is_active",
    ],
)
async def test_list_all_tracking_link_as_superuser_query_utm_params(
    client_user: Any,
    link_count: int,
    q_client: bool | None,
    q_scheme: str | None,
    q_domain: str | None,
    q_destination: str | None,
    q_url_path: str | None,
    q_campaign: str | None,
    q_medium: str | None,
    q_source: str | None,
    q_content: str | None,
    q_term: str | None,
    q_active: bool | None,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    """
    schema = http, https
    domain = example.com
    destination = https://example.com/destination
    url_path = /destination
    utm_campaign = campaign-name
    utm_medium = medium-name
    utm_source = source-name
    utm_content = content-name
    utm_term = term-name
    """
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    client_a = await create_random_client(db_session)
    client_b = await create_random_client(db_session)
    await create_random_tracking_link(
        db_session,
        client_b.id,
    )
    await create_random_tracking_link(
        db_session,
        client_b.id,
    )
    await create_random_tracking_link(db_session, client_a.id, scheme="http")
    await create_random_tracking_link(db_session, client_a.id, scheme="https")
    await create_random_tracking_link(
        db_session, client_a.id, scheme="https", domain="example.com"
    )
    await create_random_tracking_link(
        db_session,
        client_a.id,
        scheme="https",
        domain="another.com",
        path="/destination",
    )
    await create_random_tracking_link(
        db_session, client_a.id, scheme="https", path="/example-path"
    )
    await create_random_tracking_link(
        db_session, client_a.id, scheme="https", utm_campaign="campaign-name"
    )
    await create_random_tracking_link(
        db_session, client_a.id, scheme="https", utm_medium="medium-name"
    )
    await create_random_tracking_link(
        db_session, client_a.id, scheme="https", utm_source="source-name"
    )
    await create_random_tracking_link(
        db_session, client_a.id, scheme="https", utm_content="content-name"
    )
    await create_random_tracking_link(
        db_session, client_a.id, scheme="https", utm_term="term-name"
    )
    await create_random_tracking_link(
        db_session, client_a.id, scheme="https", is_active=False
    )

    query_params = {}
    if q_client:
        query_params["client_id"] = str(client_b.id)
    if q_scheme:
        query_params["scheme"] = q_scheme
    if q_domain:
        query_params["domain"] = q_domain
    if q_destination:
        query_params["destination"] = q_destination
    if q_url_path:
        query_params["url_path"] = q_url_path
    if q_campaign:
        query_params["utm_campaign"] = q_campaign
    if q_medium:
        query_params["utm_medium"] = q_medium
    if q_source:
        query_params["utm_source"] = q_source
    if q_content:
        query_params["utm_content"] = q_content
    if q_term:
        query_params["utm_term"] = q_term
    if q_active:
        query_params["is_active"] = False

    response: Response = await client.get(
        "utmlinks/",
        params=query_params,
        headers=current_user.token_headers,
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["page"] == 1
    assert data["total"] == link_count
    assert data["size"] == 1000
    assert len(data["results"]) == link_count
