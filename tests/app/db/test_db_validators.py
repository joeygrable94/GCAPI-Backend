import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import (
    optional_int_name_min_max_len,
    optional_string_domain,
    optional_string_in_list,
    optional_string_name_min_max_len,
    optional_string_utm_param,
    require_int_name_min_max_len,
    require_string_domain,
    require_string_email,
    require_string_name_min_max_len,
    required_string_in_list,
)


def test_require_int_name_min_max_len() -> None:
    test_value = require_int_name_min_max_len(v=5, name="test")
    assert test_value == 5

    with pytest.raises(ValueError):
        require_int_name_min_max_len(v=-1, name="test")

    with pytest.raises(ValueError):
        require_int_name_min_max_len(v=1, name="test", min_len=2)

    with pytest.raises(ValueError):
        require_int_name_min_max_len(v=4, name="test", max_len=2)


def test_optional_int_name_min_max_len() -> None:
    test_value = optional_int_name_min_max_len(v=5, name="test")
    assert test_value == 5

    with pytest.raises(ValueError):
        optional_int_name_min_max_len(v=-1, name="test", min_len=0)

    with pytest.raises(ValueError):
        optional_int_name_min_max_len(v=1, name="test", min_len=2)

    with pytest.raises(ValueError):
        optional_int_name_min_max_len(v=4, name="test", max_len=2)


def test_require_string_name_min_max_len() -> None:
    test_str = "hello world 15!"
    value = require_string_name_min_max_len(v=test_str, name="test")
    assert value == test_str

    with pytest.raises(ValueError):
        require_string_name_min_max_len(v="", name="test", min_len=0)

    with pytest.raises(ValueError):
        require_string_name_min_max_len(v=test_str, name="test", min_len=20)

    with pytest.raises(ValueError):
        require_string_name_min_max_len(v=test_str, name="test", max_len=5)


def test_optional_string_name_min_max_len() -> None:
    value = optional_string_name_min_max_len(v=None, name="test")
    assert value is None

    test_str = "hello world 15!"
    value = optional_string_name_min_max_len(v=test_str, name="test")
    assert value == test_str

    optional_string_name_min_max_len(v=None, name="test", min_len=0) is None

    with pytest.raises(ValueError):
        optional_string_name_min_max_len(v=test_str, name="test", min_len=20)

    with pytest.raises(ValueError):
        optional_string_name_min_max_len(v=test_str, name="test", max_len=2)


def test_require_string_domain() -> None:
    value = require_string_domain(v="getcommunity.com")
    assert value == "getcommunity.com"

    with pytest.raises(ValueError):
        require_string_domain(v="https://getcommunity.com")

    with pytest.raises(ValueError):
        require_string_domain(v="", min_len=0)

    with pytest.raises(ValueError):
        require_string_domain(v="c.co")

    with pytest.raises(ValueError):
        require_string_domain(v="asdfasdfasdfasdfc.com", min_len=40)

    with pytest.raises(ValueError):
        require_string_domain(v="asdfasdfasdfasdfc.com", max_len=20)


def test_optional_string_utm_param() -> None:
    assert optional_string_utm_param(v=None, name="utm_campaign") is None
    assert (
        optional_string_utm_param(v="valid-campaign-name", name="utm_campaign")
        == "valid-campaign-name"
    )
    with pytest.raises(ValueError):
        assert optional_string_utm_param(v="no spaces allowed", name="utm_campaign")
    with pytest.raises(ValueError):
        assert optional_string_utm_param(
            v="no*special#characters&asd", name="utm_campaign"
        )
    with pytest.raises(ValueError):
        assert optional_string_utm_param(v="1", name="utm_campaign", min_len=2)
    with pytest.raises(ValueError):
        assert optional_string_utm_param(v="", name="utm_campaign")
    with pytest.raises(ValueError):
        assert optional_string_utm_param(
            v="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1), name="utm_campaign"
        )


def test_optional_string_domain() -> None:
    value = optional_string_domain(v=None, name="test")
    assert value is None

    value = optional_string_domain(v="getcommunity.com", name="test")
    assert value == "getcommunity.com"

    with pytest.raises(ValueError):
        optional_string_domain(v="https://getcommunity.com", name="test")

    with pytest.raises(ValueError):
        optional_string_domain(v="c.co", name="test")

    with pytest.raises(ValueError):
        optional_string_domain(v=None, min_len=0, name="test")

    with pytest.raises(ValueError):
        optional_string_domain(v="asdfasdfasdfasdfc.com", min_len=40, name="test")

    with pytest.raises(ValueError):
        optional_string_domain(v="asdfasdfasdfasdfc.com", max_len=20, name="test")


def test_require_string_email() -> None:
    value = require_string_email(v="joey@getcommunity.com")
    assert value == "joey@getcommunity.com"

    with pytest.raises(ValueError):
        require_string_email(v="", min_len=0)

    with pytest.raises(ValueError):
        require_string_email(v="asdf-email-getcommunity.com")

    with pytest.raises(ValueError):
        require_string_email(v="joey@getcommunity.com", min_len=40)

    with pytest.raises(ValueError):
        require_string_email(v="joey@getcommunity.com", max_len=20)


def test_required_string_in_list() -> None:
    value = required_string_in_list(v="test", name="test", choices=["test", "test2"])
    assert value == "test"

    value = required_string_in_list(v="TEST", name="test", choices=["test", "test2"])
    assert value == "test"

    with pytest.raises(ValueError):
        required_string_in_list(v="", name="test", choices=["test2"])

    with pytest.raises(ValueError):
        required_string_in_list(v="test", name="test", choices=["test2"])


def test_optional_string_in_list() -> None:
    value = optional_string_in_list(v=None, name="test", choices=["test", "test2"])
    assert value is None

    value = optional_string_in_list(v="test", name="test", choices=["test", "test2"])
    assert value == "test"

    value = optional_string_in_list(v="TEST", name="test", choices=["test", "test2"])
    assert value == "test"

    with pytest.raises(ValueError):
        optional_string_in_list(v="", name="test", choices=["test2"])

    with pytest.raises(ValueError):
        optional_string_in_list(v="test", name="test", choices=["test2"])
