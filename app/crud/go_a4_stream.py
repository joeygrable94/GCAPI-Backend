from typing import Type

from app.crud.base import BaseRepository
from app.models import GoAnalytics4Stream
from app.schemas import (
    GoAnalytics4StreamCreate,
    GoAnalytics4StreamRead,
    GoAnalytics4StreamUpdate,
)


class GoAnalytics4StreamRepository(
    BaseRepository[
        GoAnalytics4StreamCreate,
        GoAnalytics4StreamRead,
        GoAnalytics4StreamUpdate,
        GoAnalytics4Stream,
    ]
):
    @property
    def _table(self) -> Type[GoAnalytics4Stream]:  # type: ignore
        return GoAnalytics4Stream
