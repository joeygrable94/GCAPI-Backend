from typing import Type

from app.crud.base import BaseRepository
from app.models import GoSearchConsoleDevice
from app.schemas import (
    GoSearchConsoleDeviceCreate,
    GoSearchConsoleDeviceRead,
    GoSearchConsoleDeviceUpdate,
)


class GoSearchConsoleDeviceRepository(
    BaseRepository[
        GoSearchConsoleDeviceCreate,
        GoSearchConsoleDeviceRead,
        GoSearchConsoleDeviceUpdate,
        GoSearchConsoleDevice,
    ]
):
    @property
    def _table(self) -> Type[GoSearchConsoleDevice]:  # type: ignore
        return GoSearchConsoleDevice
