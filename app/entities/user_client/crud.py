from app.core.crud import BaseRepository
from app.entities.user_client.model import UserClient
from app.entities.user_client.schemas import (
    UserClientCreate,
    UserClientRead,
    UserClientUpdate,
)


class UserClientRepository(
    BaseRepository[UserClientCreate, UserClientRead, UserClientUpdate, UserClient]
):
    @property
    def _table(self) -> UserClient:
        return UserClient
