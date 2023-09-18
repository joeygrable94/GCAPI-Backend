from typing import Type

from app.crud.base import BaseRepository
from app.models import GoSearchConsoleCountry
from app.schemas import (
    GoSearchConsoleCountryCreate,
    GoSearchConsoleCountryRead,
    GoSearchConsoleCountryUpdate,
)


class GoSearchConsoleCountryRepository(
    BaseRepository[
        GoSearchConsoleCountryCreate,
        GoSearchConsoleCountryRead,
        GoSearchConsoleCountryUpdate,
        GoSearchConsoleCountry,
    ]
):
    @property
    def _table(self) -> Type[GoSearchConsoleCountry]:  # type: ignore
        return GoSearchConsoleCountry
