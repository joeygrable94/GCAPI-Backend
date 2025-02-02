from datetime import datetime
from zoneinfo import ZoneInfo


def get_date() -> datetime:
    """generates a current datetime object

    Returns:
        datetime: current timestamp
    """
    return datetime.now()


def get_int_from_datetime(value: datetime) -> int:
    """generates a datetime value with or without timezone,
    if don't contains timezone it will managed as it is UTC

    Args:
        value (datetime): object

    Raises:
        TypeError: an invalid datetime value provided

    Returns:
        int: seconds since the Epoch
    """
    return int(value.timestamp())


def get_datetime_from_int(value: int) -> datetime:
    """generates a datetime object from an integer

    Args:
        value (int): an timetime integer

    Returns:
        datetime: object
    """
    return datetime.fromtimestamp(value)


def get_datetime_gmt_str_from_datetime(dt: datetime) -> str:
    """converts a datetime object to a string

    Args:
        dt (datetime): object

    Returns:
        str: datetime string
    """
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")
