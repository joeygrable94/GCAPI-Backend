from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
    ERROR_MESSAGE_ENTITY_RELATIONSHOP_NOT_FOUND,
)
from app.utilities.uuids import get_uuid
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.utils import random_lower_string
from tests.utils.website_keywordcorpus import create_random_website_keywordcorpus
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.anyio


async def perform_test_create(
    fake_website: bool,
    fake_page: bool,
    fake_relationship: bool,
    status_code: int,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    website = await create_random_website(db_session=db_session)
    website_id = website.id if not fake_website else get_uuid()
    if fake_relationship:
        page = await create_random_website_page(db_session, path="/")
    else:
        page = await create_random_website_page(
            db_session=db_session, website_id=website_id
        )
    page_id = page.id if not fake_page else get_uuid()
    data_in: dict[str, Any] = {
        "corpus": random_lower_string(5000),
        "rawtext": random_lower_string(10000),
        "website_id": str(website_id),
        "page_id": str(page_id),
    }
    response: Response = await client.post(
        "kwc/",
        headers=admin_user.token_headers,
        json=data_in,
    )
    data: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if error_msg is not None:
        assert error_msg in data["detail"]
    else:
        assert data["corpus"] == data_in["corpus"]
        assert data["rawtext"] == data_in["rawtext"]
        assert data["website_id"] == str(website_id)
        assert data["page_id"] == str(page_id)


async def perform_test_read(
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    website = await create_random_website(db_session=db_session)
    page = await create_random_website_page(
        db_session=db_session, website_id=website.id
    )
    website_kwc = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    response: Response = await client.get(
        f"kwc/{website_kwc.id}", headers=current_user.token_headers
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["corpus"] == website_kwc.corpus
    assert data["rawtext"] == website_kwc.rawtext
    assert data["website_id"] == str(website_kwc.website_id)
    assert data["page_id"] == str(website_kwc.page_id)


async def perform_test_delete(
    client: AsyncClient,
    db_session: AsyncSession,
    current_user: ClientAuthorizedUser,
) -> None:
    website = await create_random_website(db_session=db_session)
    page = await create_random_website_page(
        db_session=db_session, website_id=website.id
    )
    website_kwc = await create_random_website_keywordcorpus(
        db_session=db_session,
        website_id=website.id,
        page_id=page.id,
    )
    response: Response = await client.delete(
        f"kwc/{website_kwc.id}", headers=current_user.token_headers
    )
    data: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data is None


class TestListWebsiteKeywordCorpus:
    # AUTHORIZED CLIENTS
    async def test_list_all_website_page_kwc_as_superadmin(
        self,
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
        self,
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
        self,
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
        self,
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
        self,
        client: AsyncClient,
        db_session: AsyncSession,
        employee_user: ClientAuthorizedUser,
    ) -> None:
        response: Response = await client.get(
            "kwc/", headers=employee_user.token_headers
        )
        assert 200 <= response.status_code < 300
        data: Any = response.json()
        assert data["page"] == 1
        assert data["total"] == 0
        assert data["size"] == 1000
        assert len(data["results"]) == 0


class TestCreateWebsiteKeywordCorpus:
    # AUTHORIZED CLIENTS
    async def test_website_page_kwc_create_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create(
            False, False, False, 200, None, client, db_session, admin_user
        )

    async def test_website_page_kwc_create_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_create(
            False, False, False, 200, None, client, db_session, manager_user
        )

    # CASES
    async def test_website_page_kwc_create_website_not_exists(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create(
            True,
            False,
            False,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_website_page_kwc_create_website_page_not_exists(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create(
            False,
            True,
            False,
            404,
            ERROR_MESSAGE_ENTITY_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )

    async def test_website_page_kwc_create_website_page_relationship_not_found(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_create(
            False,
            False,
            True,
            404,
            ERROR_MESSAGE_ENTITY_RELATIONSHOP_NOT_FOUND,
            client,
            db_session,
            admin_user,
        )


class TestReadWebsiteKeywordCorpus:
    # AUTHORIZED CLIENTS
    async def test_read_website_page_kwc_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_read(client, db_session, admin_user)

    async def test_read_website_page_kwc_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_read(client, db_session, manager_user)

    async def test_read_website_page_kwc_as_admin_user_not_found(
        self, client, db_session, admin_user
    ) -> None:
        bad_website_kwc_id = get_uuid()
        response: Response = await client.get(
            f"kwc/{bad_website_kwc_id}", headers=admin_user.token_headers
        )
        data: dict[str, Any] = response.json()
        assert response.status_code == 404
        assert ERROR_MESSAGE_ENTITY_NOT_FOUND in data["detail"]


class TestDeleteWebsiteKeywordCorpus:
    # AUTHORIZED CLIENTS
    async def test_delete_website_page_kwc_as_admin_user(
        self, client, db_session, admin_user
    ) -> None:
        await perform_test_delete(client, db_session, admin_user)

    async def test_delete_website_page_kwc_as_manager_user(
        self, client, db_session, manager_user
    ) -> None:
        await perform_test_delete(client, db_session, manager_user)
