from typing import Any

import pytest
from tests.utils.utils import random_email, random_lower_string

from app.db.tables import User

pytestmark = pytest.mark.asyncio


async def test_user_table_valid_email() -> Any:
    email: str = random_email()
    password: str = random_lower_string()
    valid_user: Any = User(email=email, hashed_password=password)
    assert valid_user.email == email
    assert valid_user.hashed_password == password
