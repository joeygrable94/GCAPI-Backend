import pytest

from app.services.csrf import CsrfProtect


def test_csrf_protect_generate_csrf_token() -> None:
    csrf = CsrfProtect()
    csrf._secret_key = None  # type: ignore
    with pytest.raises(RuntimeError):
        csrf.generate_csrf_tokens()
