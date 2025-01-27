from app.crud.base import BaseRepository
from app.models import ClientStyleguide
from app.schemas import (
    ClientStyleguideCreate,
    ClientStyleguideRead,
    ClientStyleguideUpdate,
)


class ClientStyleguideRepository(
    BaseRepository[
        ClientStyleguideCreate,
        ClientStyleguideRead,
        ClientStyleguideUpdate,
        ClientStyleguide,
    ]
):
    @property
    def _table(self) -> ClientStyleguide:
        return ClientStyleguide
