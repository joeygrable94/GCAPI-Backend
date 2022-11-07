from typing import Any


# Users
class UsersException(Exception):
    pass


class InvalidID(UsersException):
    pass


class UserAlreadyExists(UsersException):
    pass


class UserNotExists(UsersException):
    pass


class InvalidPasswordException(UsersException):
    def __init__(self, reason: Any) -> None:
        self.reason: Any = reason  # pragma: no cover
