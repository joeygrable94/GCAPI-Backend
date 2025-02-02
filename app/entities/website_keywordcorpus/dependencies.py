from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.api.errors import EntityNotFound
from app.entities.website_keywordcorpus.crud import (
    WebsiteKeywordCorpus,
    WebsiteKeywordCorpusRepository,
)
from app.utilities import parse_id


async def get_website_page_kwc_or_404(
    db: AsyncDatabaseSession,
    kwc_id: Any,
) -> WebsiteKeywordCorpus | None:
    """Parses uuid/int and fetches website keyword corpus by id."""
    parsed_id: UUID = parse_id(kwc_id)
    website_page_kwc_repo: WebsiteKeywordCorpusRepository = (
        WebsiteKeywordCorpusRepository(session=db)
    )
    website_keyword_corpus: (
        WebsiteKeywordCorpus | None
    ) = await website_page_kwc_repo.read(parsed_id)
    if website_keyword_corpus is None:
        raise EntityNotFound(
            entity_info="WebsitePageKeywordCorpus {}".format(parsed_id)
        )
    return website_keyword_corpus


FetchWebsiteKeywordCorpusOr404 = Annotated[
    WebsiteKeywordCorpus, Depends(get_website_page_kwc_or_404)
]
