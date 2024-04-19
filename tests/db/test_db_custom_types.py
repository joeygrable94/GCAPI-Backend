import pytest
from sqlalchemy.dialects import mysql

from app.db.constants import DB_STR_BLOB_MAXLEN_STORED
from app.db.custom_types import Scopes


def test_process_bind_param_valid_scopes() -> None:
    scopes = Scopes()
    result = scopes.process_bind_param(["scope:one", "scope:two"], mysql.dialect())
    assert result == b"scope:one,scope:two"


def test_process_bind_param_invalid_scope_format() -> None:
    scopes = Scopes()
    with pytest.raises(ValueError):
        scopes.process_bind_param(["scope1", "invalid_scope"], mysql.dialect())


def test_process_bind_param_invalid_scope_too_long() -> None:
    scopes = Scopes()
    s1 = "asdf:123"
    slist = [s1 for _ in range(0, DB_STR_BLOB_MAXLEN_STORED // len(s1) + 1)]
    with pytest.raises(ValueError):
        scopes.process_bind_param(slist, mysql.dialect())


def test_process_bind_param_none_value() -> None:
    scopes = Scopes()
    result = scopes.process_bind_param(None, mysql.dialect())
    assert result == b""


def test_process_result_value_valid_scopes() -> None:
    scopes = Scopes()
    result = scopes.process_result_value(b"scope:one,scope:two", mysql.dialect())
    assert result == ["scope:one", "scope:two"]


def test_process_result_value_empty_value() -> None:
    scopes = Scopes()
    result = scopes.process_result_value(b"", mysql.dialect())
    assert result == []


def test_process_result_value_none_value() -> None:
    scopes = Scopes()
    result = scopes.process_result_value(None, mysql.dialect())
    assert result == []
