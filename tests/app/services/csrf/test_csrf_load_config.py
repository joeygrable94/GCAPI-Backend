from typing import Any

import pytest
from pydantic import ValidationError

from app.services.csrf import CsrfProtect


@pytest.mark.parametrize(
    "config_key, config_value, valid",
    [
        ("header_name", 2, False),
        ("header_name", 1.0, False),
        ("header_name", True, False),
        ("header_name", b"header_name", False),
        ("header_name", "header_name", True),
        ("header_name", [], False),
        ("header_name", {}, False),
        ("header_type", 2, False),
        ("header_type", 1.0, False),
        ("header_type", True, False),
        ("header_type", b"header_type", False),
        ("header_type", "header_type", True),
        ("header_type", [], False),
        ("header_type", {}, False),
        ("methods", 2, False),
        ("methods", 1.0, False),
        ("methods", True, False),
        ("methods", b"GET, POST", False),
        ("methods", "GET, POST", False),
        ("methods", [], True),
        ("methods", {}, False),
        ("methods", [1, 2, 3], False),
        ("methods", (1, 2, 3), False),
        ("methods", {1, 2, 3}, False),
        ("methods", ["1", "2", "3"], False),
        ("methods", ("1", "2", "3"), False),
        ("methods", {"1", "2", "3"}, False),
        ("methods", ["GET", "POST", "DELETE"], True),
        ("methods", ("GET", "POST", "DELETE"), True),
        ("methods", {"GET", "POST", "DELETE"}, True),
        ("methods", {"key": "value"}, False),
        ("secret_key", 2, False),
        ("secret_key", 1.0, False),
        ("secret_key", True, False),
        ("secret_key", b"secret", False),
        ("secret_key", "secret", True),
        ("secret_key", [], False),
        ("secret_key", {}, False),
        ("token_location", "body", True),  # missing token_key
        ("token_location", b"body", False),
        ("token_location", "header", True),
        ("token_location", b"header", False),
    ],
    ids=[
        "header_name_int",
        "header_name_float",
        "header_name_bool",
        "header_name_bytes",
        "header_name_str",
        "header_name_list",
        "header_name_dict",
        "header_type_int",
        "header_type_float",
        "header_type_bool",
        "header_type_bytes",
        "header_type_str",
        "header_type_list",
        "header_type_dict",
        "methods_int",
        "methods_float",
        "methods_bool",
        "methods_bytes",
        "methods_str",
        "methods_list",
        "methods_dict",
        "methods_list_int",
        "methods_tuple_int",
        "methods_set_int",
        "methods_list_str",
        "methods_tuple_str",
        "methods_set_str",
        "methods_list_str_valid",
        "methods_tuple_str_valid",
        "methods_set_str_valid",
        "methods_dict_str",
        "secret_key_int",
        "secret_key_float",
        "secret_key_bool",
        "secret_key_bytes",
        "secret_key_str",
        "secret_key_list",
        "secret_key_dict",
        "token_location_body_str",
        "token_location_body_bytes",
        "token_location_header_str",
        "token_location_header_bytes",
    ],
)
def test_load_config(config_key: str, config_value: Any, valid: bool) -> None:
    error_raised: bool = False
    try:

        @CsrfProtect.load_config
        def load_configs() -> list[tuple]:
            return [(config_key, config_value)]

    except Exception as err:
        error_raised = True
        assert isinstance(err, ValidationError)
    assert error_raised is (True, False)[valid]
