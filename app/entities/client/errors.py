from fastapi import status

from app.core.exceptions import ApiException
from app.entities.client.constants import (
    ERROR_MESSAGE_CLIENT_EXISTS,
    ERROR_MESSAGE_CLIENT_NOT_FOUND,
    ERROR_MESSAGE_CLIENT_RELATIONSHOP_NOT_FOUND,
)


class ClientAlreadyExists(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_CLIENT_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class ClientNotFound(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_CLIENT_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class ClientRelationshipNotFound(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_CLIENT_RELATIONSHOP_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)
