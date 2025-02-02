from app.core.crud import BaseRepository
from app.entities.client_styleguide.model import ClientStyleguide
from app.entities.client_styleguide.schemas import (
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
