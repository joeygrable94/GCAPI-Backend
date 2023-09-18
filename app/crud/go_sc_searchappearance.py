from typing import Type

from app.crud.base import BaseRepository
from app.models import GoSearchConsoleSearchappearance
from app.schemas import (
    GoSearchConsoleSearchappearanceCreate,
    GoSearchConsoleSearchappearanceRead,
    GoSearchConsoleSearchappearanceUpdate,
)


class GoSearchConsoleSearchappearanceRepository(
    BaseRepository[
        GoSearchConsoleSearchappearanceCreate,
        GoSearchConsoleSearchappearanceRead,
        GoSearchConsoleSearchappearanceUpdate,
        GoSearchConsoleSearchappearance,
    ]
):
    @property
    def _table(self) -> Type[GoSearchConsoleSearchappearance]:  # type: ignore
        return GoSearchConsoleSearchappearance
