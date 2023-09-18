from typing import Type

from app.crud.base import BaseRepository
from app.models import GoSearchConsoleQuery
from app.schemas import (
    GoSearchConsoleQueryCreate,
    GoSearchConsoleQueryRead,
    GoSearchConsoleQueryUpdate,
)


class GoSearchConsoleQueryRepository(
    BaseRepository[
        GoSearchConsoleQueryCreate,
        GoSearchConsoleQueryRead,
        GoSearchConsoleQueryUpdate,
        GoSearchConsoleQuery,
    ]
):
    @property
    def _table(self) -> Type[GoSearchConsoleQuery]:  # type: ignore
        return GoSearchConsoleQuery
