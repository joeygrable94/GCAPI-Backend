from typing import Any, List, Optional, Type, Union
from uuid import UUID

from sqlalchemy import select as sql_select

from app.core.config import settings
from app.core.utilities import paginate
from app.db.repositories.base import BaseRepository
from app.db.schemas import WebsitePageCreate, WebsitePageRead, WebsitePageUpdate
from app.db.tables import WebsitePage


class WebsitePageRepository(
    BaseRepository[WebsitePageCreate, WebsitePageRead, WebsitePageUpdate, WebsitePage]
):
    @property
    def _table(self) -> Type[WebsitePage]:  # type: ignore
        return WebsitePage

    async def _list(
        self,
        skip: int = 0,
        limit: int = settings.QUERY_DEFAULT_LIMIT_ROWS,
        website_id: UUID | None = None,
        sitemap_id: UUID | None = None
    ) -> Union[List[WebsitePage], List[None]]:
        query: Any | None = None
        if website_id is not None:
            query = (
                sql_select(self._table)
                .where(self._table.website_id == website_id)
                .offset(skip).limit(limit)
            )
        if sitemap_id is not None:
            query = (
                sql_select(self._table)
                .where(self._table.sitemap_id == sitemap_id)
                .offset(skip).limit(limit)
            )
        if website_id is not None and sitemap_id is not None:
            query = (
                sql_select(self._table)
                .where(
                    (self._table.website_id == website_id)
                    &
                    (self._table.sitemap_id == sitemap_id)
                )
                .offset(skip).limit(limit)
            )
        if query is None:
            query = sql_select(self._table).offset(skip).limit(limit)  # type: ignore
        result: Any = await self._db.execute(query)
        data: List[WebsitePage] = result.scalars().all()
        return data

    async def list(
        self, page: int = 1, website_id: UUID | None = None, sitemap_id: UUID | None = None
    ) -> Optional[Union[List[WebsitePage], List[None]]]:
        skip, limit = paginate(page)
        return await self._list(skip=skip, limit=limit, website_id=website_id, sitemap_id=sitemap_id)
