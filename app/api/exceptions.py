from typing import Any


# API Auth
class ApiAuthException(Exception):
    """
    Base except which all api authentication errors extend
    """

    def __init__(
        self,
        reason: Any,
    ) -> None:
        self.reason: Any = reason


# Generics
class EntityException(Exception):
    pass


class EntityAlreadyExists(EntityException):
    pass


class EntityNotExists(EntityException):
    pass


class InvalidID(EntityException):
    pass


class EntityIdNotProvided(EntityException):
    pass


# Users
class UsersException(EntityException):
    pass


class UserAlreadyExists(UsersException):
    pass


class UserNotExists(UsersException):
    pass


class InvalidPasswordException(UsersException):
    def __init__(self, reason: Any) -> None:
        self.reason: Any = reason


# Clients
class ClientsException(EntityException):
    pass


class ClientAlreadyExists(ClientsException):
    pass


class ClientNotExists(ClientsException):
    pass


# Websites
class WebsitesException(EntityException):
    pass


class WebsiteAlreadyExists(WebsitesException):
    pass


class WebsiteNotExists(WebsitesException):
    pass
