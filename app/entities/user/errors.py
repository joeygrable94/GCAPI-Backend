from fastapi import status

from app.core.exceptions import ApiException
from app.entities.user.constants import (
    ERROR_MESSAGE_USER_NOT_FOUND,
    ERROR_MESSAGE_USERNAME_EXISTS,
)


class UserAlreadyExists(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_USERNAME_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class UserNotFound(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_USER_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)
