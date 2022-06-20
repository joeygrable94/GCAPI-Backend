from typing import TypeVar, Protocol


ID = TypeVar("ID")


class UserProtocol(Protocol[ID]):
    """User protocol that ORM model should follow."""

    id: ID
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    def __init__(self, *args, **kwargs) -> None:
        ...  # pragma: no cover


UP = TypeVar("UP", bound=UserProtocol)
