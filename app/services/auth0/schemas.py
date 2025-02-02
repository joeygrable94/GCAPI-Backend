import os
from datetime import datetime

from pydantic import BaseModel, Field
from typing_extensions import TypedDict

auth0_rule_namespace: str = os.getenv("AUTH_RULE_NAMESPACE", "gcapi_oauth2")


class AuthUser(BaseModel):
    auth_id: str = Field(..., alias="sub")
    picture: str | None = Field(None, alias=f"{auth0_rule_namespace}/picture")
    permissions: list[str] = []
    roles: list[str] = Field([], alias=f"{auth0_rule_namespace}/roles")
    email: str = Field("", alias=f"{auth0_rule_namespace}/email")
    is_verified: bool | None = Field(None, alias=f"{auth0_rule_namespace}/is_verified")
    created: datetime | None = Field(None, alias=f"{auth0_rule_namespace}/created_on")
    updated: datetime | None = Field(None, alias=f"{auth0_rule_namespace}/updated_on")


class JwksKeyDict(TypedDict):
    kid: str
    kty: str
    use: str
    n: str
    e: str


class JwksDict(TypedDict):
    keys: list[JwksKeyDict]
