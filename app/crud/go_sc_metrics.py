from datetime import date, datetime
from typing import Any, List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, func, select as sql_select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import GoSearchConsoleMetricTypeInvalid
from app.crud.base import BaseRepository
from app.models import (
    GoSearchConsoleCountry,
    GoSearchConsoleDevice,
    GoSearchConsolePage,
    GoSearchConsoleProperty,
    GoSearchConsoleQuery,
    GoSearchConsoleSearchappearance,
)
from app.schemas import (
    GoSearchConsoleMetricCreate,
    GoSearchConsoleMetricRead,
    GoSearchConsoleMetricType,
    GoSearchConsoleMetricUpdate,
)


class GoSearchConsoleMetricRepository(
    BaseRepository[
        GoSearchConsoleMetricCreate,
        GoSearchConsoleMetricRead,
        GoSearchConsoleMetricUpdate,
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry,
    ]
):
    metric_type: GoSearchConsoleMetricType

    def __init__(self, session: AsyncSession, *args: Any, **kwargs: Any) -> None:
        super().__init__(session, *args, **kwargs)
        tmp_metric_type = kwargs.get("metric_type", None)
        if (
            tmp_metric_type is None
            or tmp_metric_type not in GoSearchConsoleMetricType.__members__
        ):
            raise GoSearchConsoleMetricTypeInvalid()
        self.metric_type = tmp_metric_type

    @property
    def _table(  # type: ignore
        self,
    ) -> Type[
        GoSearchConsoleSearchappearance
        | GoSearchConsoleQuery
        | GoSearchConsolePage
        | GoSearchConsoleDevice
        | GoSearchConsoleCountry
    ]:
        if self.metric_type == GoSearchConsoleMetricType.searchappearance:
            return GoSearchConsoleSearchappearance
        elif self.metric_type == GoSearchConsoleMetricType.query:
            return GoSearchConsoleQuery
        elif self.metric_type == GoSearchConsoleMetricType.page:
            return GoSearchConsolePage
        elif self.metric_type == GoSearchConsoleMetricType.device:
            return GoSearchConsoleDevice
        elif self.metric_type == GoSearchConsoleMetricType.country:
            return GoSearchConsoleCountry
        else:  # pragma: no cover
            raise GoSearchConsoleMetricTypeInvalid()

    def query_list(
        self,
        gsc_id: UUID | None = None,
        date_start: date | None = None,
        date_end: date | None = None,
    ) -> Select:
        # create statement joins
        stmt: Select = sql_select(self._table)
        conditions: List[BinaryExpression[bool]] = []
        if gsc_id:
            stmt.join(
                GoSearchConsoleProperty,
                self._table.gsc_id == GoSearchConsoleProperty.id,  # type: ignore
            )
            conditions.append(self._table.gsc_id.like(gsc_id))  # type: ignore
        if date_start and date_end:
            conditions.append(
                func.date(self._table.date_start).between(date_start, date_end)  # type: ignore  # noqa: E501
            )
        if date_start and not date_end:
            date_end = datetime.now().date()
            conditions.append(
                func.date(self._table.date_start).between(date_start, date_end)
            )
        if not date_start and date_end:
            date_start = date(1970, 1, 1)
            conditions.append(
                func.date(self._table.date_start).between(date_start, date_end)
            )
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
