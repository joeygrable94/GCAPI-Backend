import base64
import json
import logging
import os
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Dict, List, Optional, Type

# from jose import jwt  # type: ignore
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Depends, HTTPException, Request
from fastapi.openapi.models import OAuthFlowImplicit, OAuthFlows
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    OpenIdConnect,
    SecurityScopes,
)
from jwt.exceptions import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidSignatureError,
    InvalidTokenError,
)
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import TypedDict

from .exceptions import (
    Auth0UnauthenticatedException,
    Auth0UnauthorizedException,
    HTTPAuth0Error,
)

logger = logging.getLogger("fastapi_auth0")

auth0_rule_namespace: str = os.getenv("AUTH0_RULE_NAMESPACE", "gcapi_oauth2")

unauthenticated_response: Dict = {401: {"model": HTTPAuth0Error}}
unauthorized_response: Dict = {403: {"model": HTTPAuth0Error}}
security_responses: Dict = {**unauthenticated_response, **unauthorized_response}


def base64url_decode(input: str) -> bytes:
    rem = len(input) % 4
    if rem > 0:
        input += "=" * (4 - rem)
    return base64.urlsafe_b64decode(input)


class Auth0User(BaseModel):
    auth_id: str = Field(..., alias="sub")
    picture: Optional[str] = Field(  # type: ignore [literal-required]
        None, alias=f"{auth0_rule_namespace}/picture"
    )
    permissions: List[str] = []  # type: ignore [literal-required]
    roles: List[str] = Field(  # type: ignore [literal-required]
        [], alias=f"{auth0_rule_namespace}/roles"
    )
    email: str = Field(  # type: ignore [literal-required]
        "", alias=f"{auth0_rule_namespace}/email"
    )
    is_verified: Optional[bool] = Field(  # type: ignore [literal-required]
        None, alias=f"{auth0_rule_namespace}/is_verified"
    )
    created: Optional[datetime] = Field(  # type: ignore [literal-required]
        None, alias=f"{auth0_rule_namespace}/created_on"
    )
    updated: Optional[datetime] = Field(  # type: ignore [literal-required]
        None, alias=f"{auth0_rule_namespace}/updated_on"
    )


class Auth0HTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        return await super().__call__(request)


class OAuth2ImplicitBearer(OAuth2):
    def __init__(
        self,
        authorizationUrl: str,
        scopes: Dict[str, str] = {},
        scheme_name: Optional[str] = None,
        auto_error: bool = True,
    ):
        flows = OAuthFlows(
            implicit=OAuthFlowImplicit(authorizationUrl=authorizationUrl, scopes=scopes)
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Overwrite parent call to prevent useless overhead,
        the actual auth is done in Auth0.get_user
        This scheme is just for Swagger UI
        """
        return None


class JwksKeyDict(TypedDict):
    kid: str
    kty: str
    use: str
    n: str
    e: str


class JwksDict(TypedDict):
    keys: List[JwksKeyDict]


class Auth0:
    def __init__(
        self,
        domain: str,
        api_audience: str,
        scopes: Dict[str, str] = {},
        auto_error: bool = True,
        scope_auto_error: bool = True,
        email_auto_error: bool = False,
        auth0user_model: Type[Auth0User] = Auth0User,
    ):
        self.domain = domain
        self.audience = api_audience

        self.auto_error = auto_error
        self.scope_auto_error = scope_auto_error
        self.email_auto_error = email_auto_error

        self.auth0_user_model = auth0user_model

        self.algorithms = ["RS256"]
        r = urllib.request.urlopen(f"https://{domain}/.well-known/jwks.json")
        self.jwks: JwksDict = json.loads(r.read())

        authorization_url_qs = urllib.parse.urlencode({"audience": api_audience})
        authorization_url = f"https://{domain}/authorize?{authorization_url_qs}"
        self.implicit_scheme = OAuth2ImplicitBearer(
            authorizationUrl=authorization_url,
            scopes=scopes,
            scheme_name="Auth0ImplicitBearer",
        )
        self.password_scheme = OAuth2PasswordBearer(
            tokenUrl=f"https://{domain}/oauth/token", scopes=scopes
        )
        self.authcode_scheme = OAuth2AuthorizationCodeBearer(
            authorizationUrl=authorization_url,
            tokenUrl=f"https://{domain}/oauth/token",
            scopes=scopes,
        )
        self.oidc_scheme = OpenIdConnect(
            openIdConnectUrl=f"https://{domain}/.well-known/openid-configuration"
        )

    async def get_user(
        self,
        security_scopes: SecurityScopes,
        creds: Optional[HTTPAuthorizationCredentials] = Depends(
            Auth0HTTPBearer(auto_error=False)
        ),
    ) -> Optional[Auth0User]:
        """
        Verify the Authorization: Bearer token and return the user.
        If there is any problem and auto_error = True then
        raise Auth0UnauthenticatedException or Auth0UnauthorizedException,
        otherwise return None.

        Not to be called directly, but to be placed within a Depends() or
        Security() wrapper.

        Example: def path_op_func(user: Auth0User = Security(auth.get_user)).

        if auto_error = return 403 until solving.
        see: https://github.com/tiangolo/fastapi/pull/2120
        """
        if creds is None:
            if self.auto_error:
                raise HTTPException(403, detail="Missing bearer token")
            else:  # pragma: no cover
                return None

        token = creds.credentials
        payload: Dict = {}
        try:
            unverified_header = jwt.get_unverified_header(token)

            if "kid" not in unverified_header:
                msg = "Malformed token header"
                if self.auto_error:
                    raise Auth0UnauthenticatedException(detail=msg)
                else:  # pragma: no cover
                    logger.warning(msg)
                    return None

            rsa_key = {}
            for key in self.jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }
                    break
            if rsa_key:
                n = int.from_bytes(base64url_decode(rsa_key["n"]), "big")
                e = int.from_bytes(base64url_decode(rsa_key["e"]), "big")
                public_numbers = rsa.RSAPublicNumbers(e, n)
                public_key = public_numbers.public_key(default_backend())
                pem_key = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
                payload = jwt.decode(
                    token,
                    pem_key,
                    algorithms=self.algorithms,
                    audience=self.audience,
                    issuer=f"https://{self.domain}/",
                )
            else:  # pragma: no cover
                msg = "Invalid kid header (wrong tenant or rotated public key)"
                if self.auto_error:
                    raise Auth0UnauthenticatedException(detail=msg)
                else:
                    logger.warning(msg)
                    return None

        except ImmatureSignatureError:  # pragma: no cover
            msg = "Immature token"
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail=msg)
            else:
                logger.warning(msg)
                return None

        except ExpiredSignatureError:  # pragma: no cover
            msg = "Expired token"
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail=msg)
            else:
                logger.warning(msg)
                return None

        except InvalidSignatureError:  # pragma: no cover
            msg = "Invalid token signature"
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail=msg)
            else:
                logger.warning(msg)
                return None

        except (InvalidAudienceError, InvalidIssuerError):  # pragma: no cover
            msg = "Invalid token claims (wrong issuer or audience)"
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail=msg)
            else:
                logger.warning(msg)
                return None

        except InvalidTokenError:
            msg = "Malformed token"
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail=msg)
            else:  # pragma: no cover
                logger.warning(msg)
                return None

        except Auth0UnauthenticatedException:
            raise

        except Exception as e:  # pragma: no cover
            # This is an unlikely case but handle it just to be safe
            # (maybe the token is specially crafted to bug our code)
            logger.error(f'Handled exception decoding token: "{e}"', exc_info=True)
            if self.auto_error:
                raise Auth0UnauthenticatedException(detail="Error decoding token")
            else:
                return None

        if self.scope_auto_error:
            token_scope_str: str = payload.get("scope", "")

            if isinstance(token_scope_str, str):
                token_scopes = token_scope_str.split()

                for scope in security_scopes.scopes:
                    if scope not in token_scopes:
                        raise Auth0UnauthorizedException(
                            detail=f'Missing "{scope}" scope',
                            headers={
                                "WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'  # noqa: E501
                            },
                        )
            else:  # pragma: no cover
                # This is an unlikely case but handle it just to be safe
                # (perhaps auth0 will change the scope format)
                raise Auth0UnauthorizedException(
                    detail='Token "scope" field must be a string'
                )

        try:
            user = self.auth0_user_model(**payload)

            if self.email_auto_error and not user.email:  # pragma: no cover
                raise Auth0UnauthorizedException(
                    detail='Missing email claim (check auth0 rule "Add email to access token")'  # noqa: E501
                )

            return user

        except ValidationError as e:  # pragma: no cover
            logger.error(f'Handled exception parsing Auth0User: "{e}"', exc_info=True)
            if self.auto_error:
                raise Auth0UnauthorizedException(detail="Error parsing Auth0User")
            else:
                return None
