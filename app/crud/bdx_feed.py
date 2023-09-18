from typing import Type

from app.crud.base import BaseRepository
from app.models import BdxFeed
from app.schemas import BdxFeedCreate, BdxFeedRead, BdxFeedUpdate


class BdxFeedRepository(
    BaseRepository[BdxFeedCreate, BdxFeedRead, BdxFeedUpdate, BdxFeed]
):
    @property
    def _table(self) -> Type[BdxFeed]:  # type: ignore
        return BdxFeed
