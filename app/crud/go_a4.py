from typing import Type

from app.crud.base import BaseRepository
from app.models import GoAnalytics4Property
from app.schemas import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
    GoAnalytics4PropertyUpdate,
)


class GoAnalytics4PropertyRepository(
    BaseRepository[
        GoAnalytics4PropertyCreate,
        GoAnalytics4PropertyRead,
        GoAnalytics4PropertyUpdate,
        GoAnalytics4Property,
    ]
):
    @property
    def _table(self) -> Type[GoAnalytics4Property]:  # type: ignore
        return GoAnalytics4Property
