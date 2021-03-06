from typing import Any

from fastapi import Response, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.api import OpenAPIResponseType
from app.core.security.authentication.transport.base import (
    Transport,
    TransportLogoutNotSupportedError,
)


class BearerResponse(BaseModel):
    access_token: str
    token_type: str


class BearerTransport(Transport):
    scheme: OAuth2PasswordBearer

    def __init__(self, tokenUrl: str):
        self.scheme = OAuth2PasswordBearer(tokenUrl, auto_error=False)

    async def get_login_response(self, token: str, response: Response) -> Any:
        return BearerResponse(access_token=token, token_type="bearer")

    async def get_logout_response(self, response: Response) -> Any:
        raise TransportLogoutNotSupportedError()

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponse,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"  # allowinsecure  # noqa: E501
                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"  # allowinsecure  # noqa: E501
                            "DMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS"  # allowinsecure  # noqa: E501
                            "11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."  # allowinsecure  # noqa: E501
                            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",  # allowinsecure  # noqa: E501
                            "token_type": "bearer",
                        }
                    }
                },
            },
        }

    @staticmethod
    def get_openapi_logout_responses_success() -> OpenAPIResponseType:
        return {}
