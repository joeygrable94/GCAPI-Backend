from typing import Type

from app.crud.base import BaseRepository
from app.models import ClientBucket
from app.schemas import ClientBucketCreate, ClientBucketRead, ClientBucketUpdate


class ClientBucketRepository(
    BaseRepository[
        ClientBucketCreate, ClientBucketRead, ClientBucketUpdate, ClientBucket
    ]
):
    @property
    def _table(self) -> Type[ClientBucket]:  # type: ignore
        return ClientBucket
