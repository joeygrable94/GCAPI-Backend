from typing import Type
from uuid import UUID

from sqlalchemy import Select, and_, select as sql_select

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

    def query_list(
        self,
        website_id: UUID | None = None,
        page_id: UUID | None = None,
    ) -> Select:
        stmt: Select | None = None
        # website_id and page_id
        if website_id and page_id:
            stmt = sql_select(self._table).where(
                and_(
                    self._table.website_id == website_id, self._table.page_id == page_id
                )
            )
        # website_id only
        if website_id and page_id is None:
            stmt = sql_select(self._table).where(self._table.website_id == website_id)
        # page_id only
        if website_id is None and page_id:
            stmt = sql_select(self._table).where(self._table.page_id == page_id)
        if stmt is None:
            stmt = sql_select(self._table)
        return stmt
