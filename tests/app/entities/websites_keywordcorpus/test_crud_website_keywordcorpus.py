import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.website_keywordcorpus.crud import WebsiteKeywordCorpusRepository
from app.entities.website_keywordcorpus.model import WebsiteKeywordCorpus

pytestmark = pytest.mark.anyio


async def test_website_keyword_corpus_repo_table(db_session: AsyncSession) -> None:
    repo: WebsiteKeywordCorpusRepository = WebsiteKeywordCorpusRepository(
        session=db_session
    )
    assert repo._table is WebsiteKeywordCorpus
