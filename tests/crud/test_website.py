import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsiteRepository
from app.models import Website

pytestmark = pytest.mark.asyncio


async def test_website_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteRepository = WebsiteRepository(session=db_session)
    assert repo._table is Website


'''
async def test_website_repo_table_method_validate(db_session: AsyncSession) -> None:
    repo: WebsiteRepository = WebsiteRepository(session=db_session)
    c1: bool = await repo.validate(domain=None)
    c2: bool = await repo.validate(domain="example.com")
    c3: bool = await repo.validate(domain="https://getcommunity.com")
    c4: bool = await repo.validate(domain="getcommunity.com")
    assert not c1
    assert c2
    assert not c3
    assert c4
'''
