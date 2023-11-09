from datetime import datetime
from typing import Any
from uuid import UUID

import pytest
from pydantic import UUID4

from app.api.exceptions import InvalidID
from app.core.utilities import (
    get_date,
    get_datetime_from_int,
    get_int_from_datetime,
    get_uuid,
    get_uuid_str,
    parse_id,
)

# pytestmark = pytest.mark.asyncio


def test_get_date() -> None:
    a_date: Any = get_date()
    assert type(a_date) is datetime


def test_get_int_from_timestamp() -> None:
    now: datetime = datetime.now()
    now_int: Any = get_int_from_datetime(now)
    assert isinstance(now_int, int)


def test_get_datetime_from_int() -> None:
    past_date_num: int = 1662439917
    get_date: Any = get_datetime_from_int(past_date_num)
    assert type(get_date) is datetime


def test_get_uuid_str() -> None:
    uidstr: str = get_uuid_str()
    assert isinstance(uidstr, str)


def test_parse_id_uuid() -> None:
    uid: UUID4 = get_uuid()
    parsed_id: UUID = parse_id(uid)
    assert type(parsed_id) is UUID


def test_parse_id_uuid_str() -> None:
    uidstr: str = get_uuid_str()
    parsed_id: UUID = parse_id(uidstr)
    assert type(parsed_id) is UUID


def test_parse_id_uuid_invalid() -> None:
    not_uuid: str = "1829319274-53128309123"
    with pytest.raises(InvalidID):
        parsed_id: UUID = parse_id(not_uuid)  # noqa: F841
