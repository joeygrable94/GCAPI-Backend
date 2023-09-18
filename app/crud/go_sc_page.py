from typing import Type

from app.crud.base import BaseRepository
from app.models import GoSearchConsolePage
from app.schemas import (
    GoSearchConsolePageCreate,
    GoSearchConsolePageRead,
    GoSearchConsolePageUpdate,
)


class GoSearchConsolePageRepository(
    BaseRepository[
        GoSearchConsolePageCreate,
        GoSearchConsolePageRead,
        GoSearchConsolePageUpdate,
        GoSearchConsolePage,
    ]
):
    @property
    def _table(self) -> Type[GoSearchConsolePage]:  # type: ignore
        return GoSearchConsolePage
