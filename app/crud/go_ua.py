from typing import Type

from app.crud.base import BaseRepository
from app.models import GoUniversalAnalyticsProperty
from app.schemas import (
    GoUniversalAnalyticsPropertyCreate,
    GoUniversalAnalyticsPropertyRead,
    GoUniversalAnalyticsPropertyUpdate,
)


class GoUniversalAnalyticsPropertyRepository(
    BaseRepository[
        GoUniversalAnalyticsPropertyCreate,
        GoUniversalAnalyticsPropertyRead,
        GoUniversalAnalyticsPropertyUpdate,
        GoUniversalAnalyticsProperty,
    ]
):
    @property
    def _table(self) -> Type[GoUniversalAnalyticsProperty]:  # type: ignore
        return GoUniversalAnalyticsProperty
