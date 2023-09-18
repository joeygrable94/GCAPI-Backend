from typing import Type

from app.crud.base import BaseRepository
from app.models import GoCloudProperty
from app.schemas import (
    GoCloudPropertyCreate,
    GoCloudPropertyRead,
    GoCloudPropertyUpdate,
)


class GoCloudPropertyRepository(
    BaseRepository[
        GoCloudPropertyCreate,
        GoCloudPropertyRead,
        GoCloudPropertyUpdate,
        GoCloudProperty,
    ]
):
    @property
    def _table(self) -> Type[GoCloudProperty]:  # type: ignore
        return GoCloudProperty
