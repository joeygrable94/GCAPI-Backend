from typing import List, Type
from uuid import UUID

from sqlalchemy import Select, and_, select as sql_select

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

    def query_list(
        self,
        website_id: UUID | None = None,
        page_id: UUID | None = None,
        devices: List[str] | None = None,
    ) -> Select:
        stmt: Select | None = None
        # website_id, page_id and device strategy
        if website_id and page_id and devices:
            stmt = sql_select(self._table).where(
                and_(
                    self._table.website_id == website_id,
                    self._table.page_id == page_id,
                    self._table.strategy.in_(iter(devices)),
                )
            )
        # website_id and page_id only
        if website_id and page_id and devices is None:
            stmt = sql_select(self._table).where(
                and_(
                    self._table.website_id == website_id,
                    self._table.page_id == page_id,
                )
            )
        # website_id and strategy only
        if website_id and page_id is None and devices:
            stmt = sql_select(self._table).where(
                and_(
                    self._table.website_id == website_id,
                    self._table.strategy.in_(iter(devices)),
                )
            )
        # page_id and strategy only
        if website_id is None and page_id and devices:
            stmt = sql_select(self._table).where(
                and_(
                    self._table.page_id == page_id,
                    self._table.strategy.in_(iter(devices)),
                )
            )
        # website_id only
        if website_id and page_id is None and devices is None:
            stmt = sql_select(self._table).where(self._table.website_id == website_id)
        # page_id only
        if website_id is None and page_id and devices is None:
            stmt = sql_select(self._table).where(self._table.page_id == page_id)
        # strategy only
        if website_id is None and page_id is None and devices:
            stmt = sql_select(self._table).where(
                self._table.strategy.in_(iter(devices))
            )
        if stmt is None:
            stmt = sql_select(self._table)
        return stmt
