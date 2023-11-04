from typing import Any, List, Optional, Type, Union
from uuid import UUID

from sqlalchemy import select as sql_select

from app.core.config import settings
from app.core.utilities import paginate
from app.crud.base import BaseRepository
from app.models import WebsitePage
from app.schemas import WebsitePageCreate, WebsitePageRead, WebsitePageUpdate


class WebsitePageRepository(
    BaseRepository[WebsitePageCreate, WebsitePageRead, WebsitePageUpdate, WebsitePage]
):
    @property
    def _table(self) -> Type[WebsitePage]:  # type: ignore
        return WebsitePage

    async def _list(
        self,
        skip: int = 0,
        limit: int = settings.api.query_limit_rows_default,
        website_id: UUID | None = None,
        sitemap_id: UUID | None = None,
    ) -> Union[List[WebsitePage], List[None]]:
        query: Any | None = None
        if website_id and sitemap_id:
            query = (
                sql_select(self._table)
                .where(
                    (self._table.website_id == website_id)
                    & (self._table.sitemap_id == sitemap_id)
                )
                .offset(skip)
                .limit(limit)
            )
        if website_id and not sitemap_id:
            query = (
                sql_select(self._table)
                .where(self._table.website_id == website_id)
                .offset(skip)
                .limit(limit)
            )
        if not website_id and sitemap_id:
            query = (
                sql_select(self._table)
                .where(self._table.sitemap_id == sitemap_id)
                .offset(skip)
                .limit(limit)
            )
        if query is None:
            query = sql_select(self._table).offset(skip).limit(limit)  # type: ignore
        result: Any = await self._db.execute(query)
        data: List[WebsitePage] = result.scalars().all()  # pragma: no cover
        return data  # pragma: no cover

    async def list(
        self,
        page: int = 1,
        website_id: UUID | None = None,
        sitemap_id: UUID | None = None,
    ) -> Optional[Union[List[WebsitePage], List[None]]]:
        self._db.begin()
        skip, limit = paginate(page)
        return await self._list(
            skip=skip, limit=limit, website_id=website_id, sitemap_id=sitemap_id
        )
