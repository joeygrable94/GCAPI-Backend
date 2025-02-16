import logging
from typing import Type

from clerk_backend_api import Clerk
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

from .errors import ClerkUnauthenticatedException, ClerkUnauthorizedException
from .schemas import ClerkUser
from .utilities import decode_token

logger = logging.getLogger("clerk_auth")


class ClerkHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        return await super().__call__(request)


class ClerkAuth:
    def __init__(
        self,
        secret_key: str,
        jwks_url: str,
        issuer: str,
        pem_public_key: str,
        auto_error: bool = True,
        auth0user_model: Type[ClerkUser] = ClerkUser,
    ):
        self.secret_key = secret_key
        self.jwks_url = jwks_url
        self.issuer = issuer
        self.pem_public_key = pem_public_key
        self.algorithms = ["RS256"]

        self.auto_error = auto_error
        self.auth_user_model = auth0user_model

    async def get_user(
        self,
        creds: HTTPAuthorizationCredentials | None = Depends(
            ClerkHTTPBearer(auto_error=False)
        ),
    ) -> ClerkUser | None:
        if creds is None:
            if self.auto_error:
                raise HTTPException(403, detail="Missing bearer token")
            else:  # pragma: no cover
                return None
        token = creds.credentials
        user_details: dict = {}
        try:
            payload: dict = decode_token(
                token,
                self.jwks_url,
                self.issuer,
            )
            user_id = payload.get("user_id")
            if user_id is None:
                raise Exception("user_id not in token payload")
            clerk = Clerk(bearer_auth=self.secret_key)
            user_details = clerk.users.list(user_id=[user_id])[0]
        except Exception as e:
            logger.warning("ClerkAuth.get_user() Error:", e)
            raise ClerkUnauthenticatedException(
                detail="Error decoding user from auth token."
            )

        try:
            user = self.auth_user_model(**user_details)
            return user

        except ValidationError as e:  # pragma: no cover
            logger.error(f'Handled exception parsing ClerkUser: "{e}"', exc_info=True)
            if self.auto_error:
                raise ClerkUnauthorizedException(
                    detail="Error parsing ClerkUser details from token."
                )
            else:
                return None
