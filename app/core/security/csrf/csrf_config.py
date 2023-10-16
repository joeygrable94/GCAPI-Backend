from typing import Callable, List, Optional, Set

from pydantic import ValidationError

from app.core import logger

from .load_config import CookieSamesite, LoadConfig


class CsrfConfig(object):  # type: ignore
    _cookie_key: str = "fastapi-csrf-token"
    _cookie_path: str = "/"
    _cookie_domain: Optional[str] = None
    _cookie_samesite: Optional[CookieSamesite] = "lax"
    _cookie_secure: bool = False
    _header_name: str = "X-CSRF-Token"
    _header_type: Optional[str] = None
    _httponly: bool = True
    _max_age: int = 3600
    _methods: Set[str] = {"POST", "PUT", "PATCH", "DELETE"}
    _secret_key: str = "super-secret-key"
    _token_location: str = "header"
    _token_key: str = "csrf-token-key"

    @classmethod
    def load_config(cls, settings: Callable[..., List[tuple]]) -> None:
        try:
            config = LoadConfig(**{key.lower(): value for key, value in settings()})
            cls._cookie_key = config.cookie_key or cls._cookie_key
            cls._cookie_path = config.cookie_path or cls._cookie_path
            cls._cookie_domain = config.cookie_domain or cls._cookie_domain
            cls._cookie_samesite = config.cookie_samesite or cls._cookie_samesite
            cls._cookie_secure = config.cookie_secure or cls._cookie_secure
            cls._header_name = config.header_name or cls._header_name
            cls._header_type = config.header_type or cls._header_type
            cls._httponly = config.httponly or cls._httponly
            cls._max_age = config.max_age or cls._max_age
            cls._methods = config.methods or cls._methods
            cls._secret_key = config.secret_key or cls._secret_key
            cls._token_location = config.token_location or cls._token_location
            cls._token_key = config.token_key or cls._token_key
        except ValidationError:
            raise
        except Exception as err:
            logger.warning(err)
            raise TypeError(
                'CsrfConfig must be pydantic "BaseSettings" or list of tuple'
            )
