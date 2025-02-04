from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from tests.constants.schema import ClientAuthorizedUser
from tests.utils.website_keywordcorpus import create_random_website_keywordcorpus
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


async def test_list_all_website_page_kwc_as_superadmin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website = await create_random_website(db_session=db_session)
    page = await create_random_website_page(
        db_session=db_session, website_id=website.id
    )
    entry_1 = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    entry_2 = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    entry_3 = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    response: Response = await client.get(
        "kwc/",
        headers=admin_user.token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 3
    assert data["size"] == 1000
    assert len(data["results"]) == 3
    for entry in data["results"]:
        assert "corpus" in entry
        assert "rawtext" in entry
        assert "website_id" in entry
        assert "page_id" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["corpus"] == entry_1.corpus
            assert entry["rawtext"] == entry_1.rawtext
        if entry["id"] == str(entry_2.id):
            assert entry["corpus"] == entry_2.corpus
            assert entry["rawtext"] == entry_2.rawtext
        if entry["id"] == str(entry_3.id):
            assert entry["corpus"] == entry_3.corpus
            assert entry["rawtext"] == entry_3.rawtext


async def test_list_all_website_page_kwc_as_admin_by_website_id_and_page_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session=db_session)
    website_b = await create_random_website(db_session=db_session)
    page_a = await create_random_website_page(
        db_session=db_session, website_id=website_a.id
    )
    page_b = await create_random_website_page(
        db_session=db_session, website_id=website_b.id
    )
    page_c = await create_random_website_page(
        db_session=db_session, website_id=website_a.id
    )
    entry_1 = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_a.id,
        page_id=page_a.id,
    )
    await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_b.id,
        page_id=page_b.id,
    )
    await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_a.id,
        page_id=page_c.id,
    )
    response: Response = await client.get(
        "kwc/",
        headers=admin_user.token_headers,
        params={
            "website_id": str(website_a.id),
            "page_id": str(page_a.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 1
    assert data["size"] == 1000
    assert len(data["results"]) == 1
    for entry in data["results"]:
        assert "corpus" in entry
        assert "rawtext" in entry
        assert "website_id" in entry
        assert "page_id" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["corpus"] == entry_1.corpus
            assert entry["rawtext"] == entry_1.rawtext


async def test_list_all_website_page_kwc_as_admin_by_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session=db_session)
    website_b = await create_random_website(db_session=db_session)
    page_a = await create_random_website_page(
        db_session=db_session, website_id=website_a.id
    )
    page_b = await create_random_website_page(
        db_session=db_session, website_id=website_b.id
    )
    page_c = await create_random_website_page(
        db_session=db_session, website_id=website_a.id
    )
    entry_1 = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_a.id,
        page_id=page_a.id,
    )
    await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_b.id,
        page_id=page_b.id,
    )
    entry_3 = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_a.id,
        page_id=page_c.id,
    )
    response: Response = await client.get(
        "kwc/",
        headers=admin_user.token_headers,
        params={
            "website_id": str(website_a.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        assert "corpus" in entry
        assert "rawtext" in entry
        assert "website_id" in entry
        assert "page_id" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["corpus"] == entry_1.corpus
            assert entry["rawtext"] == entry_1.rawtext
        if entry["id"] == str(entry_3.id):
            assert entry["corpus"] == entry_3.corpus
            assert entry["rawtext"] == entry_3.rawtext


async def test_list_all_website_page_kwc_as_admin_by_page_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website_a = await create_random_website(db_session=db_session)
    website_b = await create_random_website(db_session=db_session)
    page_a = await create_random_website_page(
        db_session=db_session, website_id=website_a.id
    )
    page_b = await create_random_website_page(
        db_session=db_session, website_id=website_b.id
    )
    page_c = await create_random_website_page(
        db_session=db_session, website_id=website_a.id
    )
    entry_1 = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_a.id,
        page_id=page_a.id,
    )
    await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_b.id,
        page_id=page_b.id,
    )
    await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website_a.id,
        page_id=page_c.id,
    )
    response: Response = await client.get(
        "kwc/",
        headers=admin_user.token_headers,
        params={
            "page_id": str(page_a.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 1
    assert data["size"] == 1000
    assert len(data["results"]) == 1
    for entry in data["results"]:
        assert "corpus" in entry
        assert "rawtext" in entry
        assert "website_id" in entry
        assert "page_id" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["corpus"] == entry_1.corpus
            assert entry["rawtext"] == entry_1.rawtext


async def test_list_all_website_page_kwc_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_user: ClientAuthorizedUser,
) -> None:
    response: Response = await client.get("kwc/", headers=employee_user.token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 0
    assert data["size"] == 1000
    assert len(data["results"]) == 0
