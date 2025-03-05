import pytest

from app.services.permission import Scope

pytestmark = pytest.mark.anyio


async def test_permission_scope_type() -> None:
    scope = Scope("role:user")
    assert scope == "role:user"
    """
    invalid_scope: str = "invalid-format"
    with pytest.raises(ValueError):
        Scope(invalid_scope)
    """
