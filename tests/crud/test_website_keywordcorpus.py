import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories import WebsiteKeywordCorpusRepository
from app.db.tables import WebsiteKeywordCorpus

pytestmark = pytest.mark.asyncio


async def test_websites_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteKeywordCorpusRepository = WebsiteKeywordCorpusRepository(session=db_session)
    assert repo._table is WebsiteKeywordCorpus
