from fastapi import status

from app.core.exceptions import ApiException
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
    ERROR_MESSAGE_ENTITY_RELATIONSHOP_NOT_FOUND,
    ERROR_MESSAGE_ID_INVALID,
)


class InvalidID(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_ID_INVALID):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message)


class EntityAlreadyExists(ApiException):
    def __init__(
        self, message: str = ERROR_MESSAGE_ENTITY_EXISTS, entity_info: str = "DataModel"
    ):
        super().__init__(status.HTTP_400_BAD_REQUEST, message + f": {entity_info}")


class EntityNotFound(ApiException):
    def __init__(
        self,
        message: str = ERROR_MESSAGE_ENTITY_NOT_FOUND,
        entity_info: str = "DataModel",
    ):
        super().__init__(status.HTTP_404_NOT_FOUND, message + f": {entity_info}")


class EntityRelationshipNotFound(ApiException):
    def __init__(
        self,
        message: str = ERROR_MESSAGE_ENTITY_RELATIONSHOP_NOT_FOUND,
        entity_info: str = "DataModel",
    ):
        super().__init__(status.HTTP_404_NOT_FOUND, message + f": {entity_info}")
