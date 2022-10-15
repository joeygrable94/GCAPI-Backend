from typing import Any


# DB Entities
class EntityException(Exception):
    pass


class EntityAlreadyExists(Exception):
    pass


class EntityNotExists(Exception):
    pass


# Users
class UsersException(Exception):
    pass


class InvalidID(UsersException):
    pass


class UserAlreadyExists(UsersException):
    pass


class UserNotExists(UsersException):
    pass


class UserInactive(UsersException):
    pass


class UserEmailUnverified(UsersException):
    pass


class UserAlreadyVerified(UsersException):
    pass


class InvalidVerifyToken(UsersException):
    pass


class InvalidResetPasswordToken(UsersException):
    pass


class InvalidPasswordException(UsersException):
    def __init__(self, reason: Any) -> None:
        self.reason: Any = reason  # pragma: no cover
