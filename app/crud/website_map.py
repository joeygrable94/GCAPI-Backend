from typing import Any, List, Optional, Type, Union
from uuid import UUID

from sqlalchemy import select as sql_select

from app.core.config import settings
from app.core.utilities import paginate
from app.crud.base import BaseRepository
from app.models import WebsiteMap
from app.schemas import WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate


class WebsiteMapRepository(
    BaseRepository[WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate, WebsiteMap]
):
    @property
    def _table(self) -> Type[WebsiteMap]:  # type: ignore
        return WebsiteMap

    async def _list(
        self,
        skip: int = 0,
        limit: int = settings.api.query_limit_rows_default,
        website_id: UUID | None = None,
    ) -> Union[List[WebsiteMap], List[None]]:
        query: Any | None = None
        if website_id:
            query = (
                sql_select(self._table)
                .where(self._table.website_id == website_id)
                .offset(skip)
                .limit(limit)
            )
        if query is None:
            query = sql_select(self._table).offset(skip).limit(limit)  # type: ignore
        result: Any = await self._db.execute(query)
        data: List[WebsiteMap] = result.scalars().all()  # pragma: no cover
        return data  # pragma: no cover

    async def list(
        self,
        page: int = 1,
        website_id: UUID | None = None,
    ) -> Optional[Union[List[WebsiteMap], List[None]]]:
        self._db.begin()
        skip, limit = paginate(page)
        return await self._list(skip=skip, limit=limit, website_id=website_id)
