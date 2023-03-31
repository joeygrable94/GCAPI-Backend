import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import WebsiteKeywordCorpusRepository
from app.models import WebsiteKeywordCorpus

pytestmark = pytest.mark.asyncio


async def test_website_keyword_corpus_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteKeywordCorpusRepository = WebsiteKeywordCorpusRepository(
        session=db_session
    )
    assert repo._table is WebsiteKeywordCorpus
