from typing import Any, List, Optional, Type, Union
from uuid import UUID

from sqlalchemy import select as sql_select

from app.core.config import settings
from app.core.utilities import paginate
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

    async def _list(
        self,
        skip: int = 0,
        limit: int = settings.api.query_limit_rows_default,
        website_id: UUID | None = None,
        page_id: UUID | None = None,
    ) -> Union[List[WebsiteKeywordCorpus], List[None]]:
        query: Any | None = None
        # website_id, and page_id
        if website_id and page_id:
            query = (
                sql_select(self._table)
                .where(
                    (self._table.website_id == website_id)
                    & (self._table.page_id == page_id)
                )
                .offset(skip)
                .limit(limit)
            )
        # website_id only
        if website_id and page_id is None:
            query = (
                sql_select(self._table)
                .where(self._table.website_id == website_id)
                .offset(skip)
                .limit(limit)
            )
        # page_id only
        if website_id is None and page_id:
            query = (
                sql_select(self._table)
                .where(self._table.page_id == page_id)
                .offset(skip)
                .limit(limit)
            )
        if query is None:
            query = sql_select(self._table).offset(skip).limit(limit)  # type: ignore
        result: Any = await self._db.execute(query)
        data: List[WebsiteKeywordCorpus] = result.scalars().all()  # pragma: no cover
        return data  # pragma: no cover

    async def list(
        self,
        page: int = 1,
        website_id: UUID | None = None,
        page_id: UUID | None = None,
    ) -> Optional[Union[List[WebsiteKeywordCorpus], List[None]]]:
        skip, limit = paginate(page)
        return await self._list(
            skip=skip,
            limit=limit,
            website_id=website_id,
            page_id=page_id,
        )
