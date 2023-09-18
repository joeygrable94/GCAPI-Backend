from typing import Type

from app.crud.base import BaseRepository
from app.models import FileAsset
from app.schemas import FileAssetCreate, FileAssetRead, FileAssetUpdate


class FileAssetRepository(
    BaseRepository[FileAssetCreate, FileAssetRead, FileAssetUpdate, FileAsset]
):
    @property
    def _table(self) -> Type[FileAsset]:  # type: ignore
        return FileAsset
