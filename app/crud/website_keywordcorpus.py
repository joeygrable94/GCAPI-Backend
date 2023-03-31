from typing import Type

from app.crud.base import BaseRepository
from app.models import WebsiteKeywordCorpus
from app.schemas import (
    WebsiteKeywordCorpusCreate,
    WebsiteKeywordCorpusRead,
    WebsiteKeywordCorpusUpdate,
)


class WebsiteKeywordCorpusRepository(
    BaseRepository[
        WebsiteKeywordCorpusCreate,
        WebsiteKeywordCorpusRead,
        WebsiteKeywordCorpusUpdate,
        WebsiteKeywordCorpus,
    ]
):
    @property
    def _table(self) -> Type[WebsiteKeywordCorpus]:  # type: ignore
        return WebsiteKeywordCorpus
