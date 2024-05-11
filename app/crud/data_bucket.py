from typing import Type

from app.crud.base import BaseRepository
from app.models import DataBucket
from app.schemas import DataBucketCreate, DataBucketRead, DataBucketUpdate


class DataBucketRepository(
    BaseRepository[DataBucketCreate, DataBucketRead, DataBucketUpdate, DataBucket]
):
    @property
    def _table(self) -> Type[DataBucket]:  # type: ignore
        return DataBucket
