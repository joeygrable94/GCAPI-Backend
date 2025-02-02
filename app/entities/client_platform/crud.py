from app.core.crud import BaseRepository
from app.entities.client_platform.model import ClientPlatform
from app.entities.client_platform.schemas import (
    ClientPlatformCreate,
    ClientPlatformRead,
    ClientPlatformUpdate,
)


class ClientPlatformRepository(
    BaseRepository[
        ClientPlatformCreate, ClientPlatformRead, ClientPlatformUpdate, ClientPlatform
    ]
):
    @property
    def _table(self) -> ClientPlatform:
        return ClientPlatform
