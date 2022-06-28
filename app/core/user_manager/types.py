from typing import (Any, AsyncGenerator, Callable, Coroutine, Generator,
                    Protocol, TypeVar, Union)

RETURN_TYPE = TypeVar("RETURN_TYPE")

DependencyCallable: Any = Callable[
    ...,
    Union[
        RETURN_TYPE,
        Coroutine[None, None, RETURN_TYPE],
        AsyncGenerator[RETURN_TYPE, None],
        Generator[RETURN_TYPE, None, None],
    ],
]


ID = TypeVar("ID")


class UserProtocol(Protocol[ID]):
    """User protocol the ORM model should follow."""

    id: ID
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...  # pragma: no cover


UP = TypeVar("UP", bound=UserProtocol)
