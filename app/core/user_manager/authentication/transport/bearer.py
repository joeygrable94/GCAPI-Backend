from typing import Any

from fastapi import Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.core.user_manager.authentication.transport.base import (
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
