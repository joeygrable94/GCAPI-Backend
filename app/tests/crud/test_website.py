from typing import Any, Optional

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import WebsitesRepository
from app.db.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate
from app.tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


async def test_create_website(db_session: AsyncSession) -> None:
    domain: str = random_lower_string()
    is_secure: bool = False
    website_repo: WebsitesRepository = WebsitesRepository(session=db_session)
    website: WebsiteRead = await website_repo.create(
        WebsiteCreate(domain=domain, is_secure=is_secure)
    )
    assert website.domain == domain
    assert website.is_secure == is_secure


async def test_get_website(
    db_session: AsyncSession,
) -> None:
    domain: str = random_lower_string()
    is_secure: bool = False
    website_repo: WebsitesRepository = WebsitesRepository(session=db_session)
    website: WebsiteRead = await website_repo.create(
        WebsiteCreate(domain=domain, is_secure=is_secure)
    )
    stored_website: Optional[WebsiteRead] = await website_repo.read(entry_id=website.id)
    assert stored_website
    assert website.id == stored_website.id
    assert website.domain == stored_website.domain
    assert website.is_secure == stored_website.is_secure


async def test_update_website(
    db_session: AsyncSession,
) -> None:
    domain: str = random_lower_string()
    is_secure: bool = False
    website_repo: WebsitesRepository = WebsitesRepository(session=db_session)
    website: WebsiteRead = await website_repo.create(
        WebsiteCreate(domain=domain, is_secure=is_secure)
    )
    is_secure2: bool = True
    website2: Optional[WebsiteRead] = await website_repo.update(
        entry_id=website.id, schema=WebsiteUpdate(is_secure=is_secure2)
    )
    assert website is not None
    assert website2 is not None
    assert website.id == website2.id
    assert website.domain == website2.domain
    assert website2.is_secure == is_secure2


async def test_delete_website(
    db_session: AsyncSession,
) -> None:
    domain: str = random_lower_string()
    is_secure: bool = False
    website_repo: WebsitesRepository = WebsitesRepository(session=db_session)
    website: WebsiteRead = await website_repo.create(
        WebsiteCreate(domain=domain, is_secure=is_secure)
    )
    website2: Any = await website_repo.delete(entry_id=website.id)
    website3: Any = await website_repo.read(entry_id=website.id)
    assert website2.id == website.id
    assert website2.domain == domain
    assert website2.is_secure == is_secure
    assert website3 is None
