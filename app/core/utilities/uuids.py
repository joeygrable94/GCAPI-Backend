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
    except ValueError as e:
        raise InvalidID() from e


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
    USERNAME_MAX_LENGTH = 255
    allowed_characters = string.ascii_letters + string.digits + "_"
    max_username_length = min(USERNAME_MAX_LENGTH, len(allowed_characters))
    username_length = random.randint(1, max_username_length)
    username = "".join(
        random.choice(allowed_characters) for _ in range(username_length)
    )
    return username
