from typing import Any

import pytest

from app.db.tables import User
from tests.utils.utils import random_email, random_lower_string

pytestmark = pytest.mark.anyio


async def test_user_table_valid_email() -> Any:
    email: str = random_email()
    password: str = random_lower_string()
    valid_user: Any = User(email=email, hashed_password=password)
    assert valid_user.email == email
    assert valid_user.hashed_password == password


async def test_user_table_invalid_email() -> Any:
    password: str = random_lower_string()
    with pytest.raises(ValueError):
        invalid_user: Any = User(  # noqa: F841
            email="notanemailstr", hashed_password=password
        )


async def test_user_table_invalid_provider() -> Any:
    password: str = random_lower_string()
    with pytest.raises(ValueError):
        invalid_user: Any = User(  # noqa: F841
            email="user@invaliddomain.com", hashed_password=password
        )
