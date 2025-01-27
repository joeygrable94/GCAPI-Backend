from app.crud.base import BaseRepository
from app.models import ClientPlatform
from app.schemas import ClientPlatformCreate, ClientPlatformRead, ClientPlatformUpdate


class ClientPlatformRepository(
    BaseRepository[
        ClientPlatformCreate, ClientPlatformRead, ClientPlatformUpdate, ClientPlatform
    ]
):
    @property
    def _table(self) -> ClientPlatform:
        return ClientPlatform
