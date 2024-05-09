import random
import string
import uuid
from typing import Any

from pydantic import UUID4

from app.api.exceptions import InvalidID


def parse_id(value: Any) -> UUID4:
    if isinstance(value, uuid.UUID):
        return value
    try:
        return uuid.UUID(value)
    except ValueError:
        raise InvalidID()


def get_uuid() -> UUID4:
    """generates a UUID object

    Returns:
        UUID4: object
    """
    return uuid.uuid4()


def get_uuid_str() -> str:
    """generates a UUID string

    Returns:
        str: stringified UUID
    """
    return str(get_uuid())


def get_random_username() -> str:
    """generates a random username

    Returns:
        str: string
    """
    username = "".join(random.choices(string.ascii_lowercase, k=64))
    return username
