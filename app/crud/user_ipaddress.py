from app.crud.base import BaseRepository
from app.models import UserIpaddress
from app.schemas import UserIpaddressCreate, UserIpaddressRead, UserIpaddressUpdate


class UserIpaddressRepository(
    BaseRepository[
        UserIpaddressCreate, UserIpaddressRead, UserIpaddressUpdate, UserIpaddress
    ]
):
    @property
    def _table(self) -> UserIpaddress:
        return UserIpaddress
