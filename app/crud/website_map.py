from typing import Type
from uuid import UUID

from sqlalchemy import Select, select as sql_select

from app.crud.base import BaseRepository
from app.models import WebsiteMap
from app.schemas import WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate


class WebsiteMapRepository(
    BaseRepository[WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate, WebsiteMap]
):
    @property
    def _table(self) -> Type[WebsiteMap]:  # type: ignore
        return WebsiteMap

    def query_list(
        self,
        website_id: UUID | None = None,
    ) -> Select:
        stmt: Select | None = None
        if website_id:
            stmt = sql_select(self._table).where(self._table.website_id == website_id)
        if stmt is None:
            stmt = sql_select(self._table)
        return stmt
