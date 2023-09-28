from typing import Any, List, Optional, Type, Union
from uuid import UUID

from sqlalchemy import select as sql_select

from app.core.config import settings
from app.core.utilities import paginate
from app.crud.base import BaseRepository
from app.models import WebsitePageSpeedInsights
from app.schemas import (
    WebsitePageSpeedInsightsCreate,
    WebsitePageSpeedInsightsRead,
    WebsitePageSpeedInsightsUpdate,
)


class WebsitePageSpeedInsightsRepository(
    BaseRepository[
        WebsitePageSpeedInsightsCreate,
        WebsitePageSpeedInsightsRead,
        WebsitePageSpeedInsightsUpdate,
        WebsitePageSpeedInsights,
    ]
):
    @property
    def _table(self) -> Type[WebsitePageSpeedInsights]:  # type: ignore
        return WebsitePageSpeedInsights

    async def _list(
        self,
        skip: int = 0,
        limit: int = settings.QUERY_DEFAULT_LIMIT_ROWS,
        website_id: UUID | None = None,
        page_id: UUID | None = None,
        devices: List[str] | None = None,
    ) -> Union[List[WebsitePageSpeedInsights], List[None]]:
        query: Any | None = None
        # website_id, page_id and device strategy
        if website_id and page_id and devices:
            query = (
                sql_select(self._table)
                .where(
                    (self._table.website_id == website_id)
                    & (self._table.page_id == page_id)
                    & (self._table.strategy.in_(iter(devices)))
                )
                .offset(skip)
                .limit(limit)
            )
        # website_id and page_id only
        if website_id and page_id and devices is None:
            query = (
                sql_select(self._table)
                .where(
                    (self._table.website_id == website_id)
                    & (self._table.page_id == page_id)
                )
                .offset(skip)
                .limit(limit)
            )
        # website_id and strategy only
        if website_id and page_id is None and devices:
            query = (
                sql_select(self._table)
                .where(
                    (self._table.website_id == website_id)
                    & (self._table.strategy.in_(iter(devices)))
                )
                .offset(skip)
                .limit(limit)
            )
        # page_id and strategy only
        if website_id is None and page_id and devices:
            query = (
                sql_select(self._table)
                .where(
                    (self._table.page_id == page_id)
                    & (self._table.strategy.in_(iter(devices)))
                )
                .offset(skip)
                .limit(limit)
            )
        # website_id only
        if website_id and page_id is None and devices is None:
            query = (
                sql_select(self._table)
                .where(self._table.website_id == website_id)
                .offset(skip)
                .limit(limit)
            )
        # page_id only
        if website_id is None and page_id and devices is None:
            query = (
                sql_select(self._table)
                .where(self._table.page_id == page_id)
                .offset(skip)
                .limit(limit)
            )
        # strategy only
        if website_id is None and page_id is None and devices:
            query = (
                sql_select(self._table)
                .where(self._table.strategy.in_(iter(devices)))
                .offset(skip)
                .limit(limit)
            )
        if query is None:
            query = sql_select(self._table).offset(skip).limit(limit)  # type: ignore
        result: Any = await self._db.execute(query)
        data: List[
            WebsitePageSpeedInsights
        ] = result.scalars().all()  # pragma: no cover
        return data  # pragma: no cover

    async def list(
        self,
        page: int = 1,
        website_id: UUID | None = None,
        page_id: UUID | None = None,
        devices: List[str] | None = None,
    ) -> Optional[Union[List[WebsitePageSpeedInsights], List[None]]]:
        skip, limit = paginate(page)
        return await self._list(
            skip=skip,
            limit=limit,
            website_id=website_id,
            page_id=page_id,
            devices=devices,
        )
