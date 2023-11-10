from typing import Type
from uuid import UUID

from sqlalchemy import Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import WebsitePage
from app.schemas import WebsitePageCreate, WebsitePageRead, WebsitePageUpdate


class WebsitePageRepository(
    BaseRepository[WebsitePageCreate, WebsitePageRead, WebsitePageUpdate, WebsitePage]
):
    @property
    def _table(self) -> Type[WebsitePage]:  # type: ignore
        return WebsitePage

    def query_list(
        self,
        website_id: UUID | None = None,
        sitemap_id: UUID | None = None,
    ) -> Select:
        stmt: Select | None = None
        # website_id and sitemap_id
        if website_id and sitemap_id:
            stmt = sql_select(self._table).where(
                and_(
                    self._table.website_id == website_id,
                    self._table.sitemap_id == sitemap_id,
                )
            )
        # only website_id
        if website_id and not sitemap_id:
            stmt = sql_select(self._table).where(self._table.website_id == website_id)
        # only sitemap_id
        if not website_id and sitemap_id:
            stmt = sql_select(self._table).where(self._table.sitemap_id == sitemap_id)
        if stmt is None:
            stmt = sql_select(self._table)
        return stmt
