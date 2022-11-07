from datetime import datetime
from typing import Optional


def get_date() -> datetime:
    """generates a current datetime object

    Returns:
        datetime: current timestamp
    """
    return datetime.now()


def get_int_from_datetime(value: Optional[datetime]) -> int:
    """generates a datetime value with or without timezone,
    if don't contains timezone it will managed as it is UTC

    Args:
        value (datetime): object

    Raises:
        TypeError: an invalid datetime value provided

    Returns:
        int: seconds since the Epoch
    """
    if not isinstance(value, datetime):  # pragma: no cover
        raise TypeError("a datetime is required")
    return int(value.timestamp())


def get_datetime_from_int(value: int) -> datetime:
    """generates a datetime object from an integer

    Args:
        value (int): an timetime integer

    Returns:
        datetime: object
    """
    if not isinstance(value, int):  # pragma: no cover
        raise TypeError("an integer is required")
    return datetime.fromtimestamp(value)
