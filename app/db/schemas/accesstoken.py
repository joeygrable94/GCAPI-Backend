from datetime import datetime
from typing import Optional, Sequence, Union

from pydantic import UUID4, BaseModel, validator

from app.db.acls.accesstoken import AccessTokenACL
from app.db.schemas.base import BaseSchema, BaseSchemaRead


# validators
class ValidateAccessTokenIdentifiers(BaseSchema):  # pragma: no cover
    token_jti: str
    csrf: str

    @validator("token_jti")
    def limits_token_jti(cls, v: str) -> str:
        if len(v) > 64:
            raise ValueError("token identifiers must contain less than 64 characters")
        return v

    @validator("csrf")
    def limits_csrf(cls, v: str) -> str:
        if len(v) > 64:
            raise ValueError("token csrf must contain less than 64 characters")
        return v


# JWT Bearer Response
class BearerResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str = ""
    access_token_csrf: str = ""
    refresh_token: Optional[str] = None
    refresh_token_csrf: Optional[str] = None


# JWT
class BaseToken(BaseModel):
    """
    type (access/refresh): the type of token issued
    iss (issuer): Issuer of the JWT
    nbf (not before time): Time before which the JWT must not be accepted
    iat (issued at time): Time at which the JWT was issued;
        can be used to determine age of the JWT
    jti (unique ID): allows a token to ID-ed by its user
    """

    type: str
    iss: str
    nbf: int
    iat: int
    jti: str


class JWToken(BaseToken):
    """
    sub (subject): Subject of the JWT (the user)
    aud (audience): Recipient for which the JWT is intended
    exp (expiration time): Time after which the JWT expires
    fresh (True/False): whether a token is in "fresh" states
    csrf (unique ID): used to prevent the use of forged tokens
    """

    type: str
    iss: str
    nbf: int
    iat: int
    jti: str
    sub: Optional[Union[str, int]]
    aud: Optional[Union[str, Sequence[str]]]
    exp: Optional[datetime]
    fresh: Optional[bool]
    csrf: Optional[str]


# DB JWT
class AccessTokenInDB(ValidateAccessTokenIdentifiers):
    token_jti: str
    csrf: str
    expires_at: Optional[datetime]
    is_revoked: bool
    user_id: UUID4


# schemas
class AccessTokenCreate(ValidateAccessTokenIdentifiers):
    token_jti: str
    csrf: str
    expires_at: Optional[datetime]
    is_revoked: bool = False
    user_id: UUID4


class AccessTokenUpdate(BaseSchema):
    is_revoked: Optional[bool] = True


class AccessTokenRead(AccessTokenACL, ValidateAccessTokenIdentifiers, BaseSchemaRead):
    token_jti: str
    csrf: str
    expires_at: Optional[datetime]
    is_revoked: bool
    user_id: UUID4
