from typing import Any


# Generics
class EntityException(Exception):
    pass


class EntityAlreadyExists(EntityException):
    pass


class EntityNotExists(EntityException):
    pass


class InvalidID(EntityException):
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
