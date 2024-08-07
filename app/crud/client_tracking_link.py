from typing import Type

from app.crud.base import BaseRepository
from app.models import ClientTrackingLink
from app.schemas import (
    ClientTrackingLinkCreate,
    ClientTrackingLinkRead,
    ClientTrackingLinkUpdate,
)


class ClientTrackingLinkRepository(
    BaseRepository[
        ClientTrackingLinkCreate,
        ClientTrackingLinkRead,
        ClientTrackingLinkUpdate,
        ClientTrackingLink,
    ]
):
    @property
    def _table(self) -> Type[ClientTrackingLink]:  # type: ignore
        return ClientTrackingLink
