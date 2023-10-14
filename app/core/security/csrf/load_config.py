from typing import Annotated, Any, Dict, Literal, Optional, Set

from pydantic import BaseModel, StrictBool, StrictInt, StrictStr, field_validator

CookieSamesite = Annotated[Literal["lax", "strict", "none"], "cookie_samesite"]


class LoadConfig(BaseModel):
    cookie_key: Optional[StrictStr] = "fastapi-csrf-token"
    cookie_path: Optional[StrictStr] = "/"
    cookie_domain: Optional[StrictStr] = None
    # NOTE: `cookie_secure` must be placed before `cookie_samesite`
    cookie_secure: Optional[StrictBool] = False
    cookie_samesite: Optional[CookieSamesite] = "lax"
    header_name: Optional[StrictStr] = "X-CSRF-Token"
    header_type: Optional[StrictStr] = None
    httponly: Optional[StrictBool] = True
    max_age: Optional[StrictInt] = 3600
    methods: Optional[Set[StrictStr]] = {"POST", "PUT", "PATCH", "DELETE"}
    secret_key: Optional[StrictStr] = None
    token_location: Optional[StrictStr] = "header"
    token_key: Optional[StrictStr] = "csrf-token-key"

    @field_validator("methods")
    def validate_csrf_methods(cls, value: str) -> str:
        if value.upper() not in {"GET", "HEAD", "POST", "PUT", "DELETE", "PATCH"}:
            raise ValueError('The "csrf_methods" must be between http request methods')
        return value.upper()

    @field_validator("cookie_samesite")  # type: ignore
    def validate_cookie_samesite(
        cls, value: CookieSamesite, values: Dict[str, Any]
    ) -> CookieSamesite:  # noqa: E501
        if value not in {"strict", "lax", "none"}:
            raise ValueError(
                'The "cookie_samesite" must be between "strict", "lax", or "none".'
            )
        elif value == "none" and values.get("cookie_secure", False) is not True:
            raise ValueError(
                'The "cookie_secure" must be True if "cookie_samesite" set to "none".'
            )
        return value

    @field_validator("token_location")
    def validate_token_location(cls, value: str) -> str:
        if value not in {"body", "header"}:
            raise ValueError('The "token_location" must be either "body" or "header".')
        return value
