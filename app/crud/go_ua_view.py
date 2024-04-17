from typing import Type

from app.crud.base import BaseRepository
from app.models import GoUniversalAnalyticsView
from app.schemas import (
    GoUniversalAnalyticsViewCreate,
    GoUniversalAnalyticsViewRead,
    GoUniversalAnalyticsViewUpdate,
)


class GoUniversalAnalyticsViewRepository(
    BaseRepository[
        GoUniversalAnalyticsViewCreate,
        GoUniversalAnalyticsViewRead,
        GoUniversalAnalyticsViewUpdate,
        GoUniversalAnalyticsView,
    ]
):
    @property
    def _table(self) -> Type[GoUniversalAnalyticsView]:  # type: ignore
        return GoUniversalAnalyticsView
