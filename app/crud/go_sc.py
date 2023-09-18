from typing import Type

from app.crud.base import BaseRepository
from app.models import GoSearchConsoleProperty
from app.schemas import (
    GoSearchConsolePropertyCreate,
    GoSearchConsolePropertyRead,
    GoSearchConsolePropertyUpdate,
)


class GoSearchConsolePropertyRepository(
    BaseRepository[
        GoSearchConsolePropertyCreate,
        GoSearchConsolePropertyRead,
        GoSearchConsolePropertyUpdate,
        GoSearchConsoleProperty,
    ]
):
    @property
    def _table(self) -> Type[GoSearchConsoleProperty]:  # type: ignore
        return GoSearchConsoleProperty
