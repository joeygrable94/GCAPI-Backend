from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import WebsiteKeywordCorpusCreate, WebsiteKeywordCorpusRead, WebsiteKeywordCorpusUpdate
from app.db.tables import WebsiteKeywordCorpus


class WebsiteKeywordCorpusRepository(
    BaseRepository[WebsiteKeywordCorpusCreate, WebsiteKeywordCorpusRead, WebsiteKeywordCorpusUpdate, WebsiteKeywordCorpus]
):
    @property
    def _table(self) -> Type[WebsiteKeywordCorpus]:  # type: ignore
        return WebsiteKeywordCorpus
