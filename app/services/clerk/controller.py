import json
import logging
from typing import Type

import jwt
from clerk_backend_api import Clerk
from clerk_backend_api.models.user import User
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

from app.config import ApiModes, settings

from .errors import ClerkUnauthenticatedException, ClerkUnauthorizedException
from .schemas import ClerkUser

logger = logging.getLogger("clerk_auth")


class ClerkHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        return await super().__call__(request)


class ClerkAuth:
    def __init__(
        self,
        secret_key: str,
        issuer: str,
        pem_public_key: str,
        auto_error: bool = True,
        user_model: Type[ClerkUser] = ClerkUser,
    ):
        self.secret_key = secret_key
        self.issuer = issuer
        public_key = json.loads(pem_public_key)
        self.pem_public_key = public_key["public_key"]
        self.algorithms = ["RS256"]

        self.auto_error = auto_error
        self.auth_user_model = user_model

        # self.implicit_scheme = HTTPAuthorizationCredentials(
        #     scheme_name="ClerkHTTPBearer",
        # )

    async def get_user(
        self,
        creds: HTTPAuthorizationCredentials | None = Depends(
            ClerkHTTPBearer(auto_error=False)
        ),
    ) -> ClerkUser | None:
        if creds is None:  # pragma: no cover
            if self.auto_error:
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN, detail="Missing bearer token"
                )
            else:
                return None
        token = creds.credentials
        token_data: dict = {}
        try:
            token_data = jwt.decode(
                token,
                self.pem_public_key,
                algorithms=["RS256"],
                issuer=self.issuer,
            )
            user_id = token_data.get("sub", None)
            if user_id is None:  # pragma: no cover
                raise Exception("user_id not in token payload")
            if settings.api.mode != ApiModes.test.value:  # pragma: no cover
                clerk = Clerk(bearer_auth=self.secret_key)
                users: list[User] | None = clerk.users.list(user_id=[user_id])
                if len(users) == 0:
                    raise Exception("User not found")
            return self.auth_user_model(**token_data)
        except ValidationError as e:  # pragma: no cover
            logger.error(f'Handled exception parsing ClerkUser: "{e}"', exc_info=True)
            if self.auto_error:
                raise ClerkUnauthorizedException(
                    detail="Error parsing ClerkUser details from token."
                )
            else:
                return None
        except Exception:  # pragma: no cover
            if self.auto_error:
                raise ClerkUnauthenticatedException(
                    detail="Error decoding user from auth token."
                )
            else:
                return None
