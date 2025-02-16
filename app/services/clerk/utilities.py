import logging
from typing import Any

import jwt
import requests

logger = logging.getLogger("clerk_auth")


def get_jwks(url: str) -> dict[str, Any]:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_public_key(jwks_url: str, kid: str) -> str:
    jwks = get_jwks(jwks_url)
    for keys in jwks["keys"]:
        if keys["kid"] == kid:
            return jwt.encode(keys, algorithm="RS256")
    raise ValueError("Invalid Clerk Token")


def decode_token(
    token: str,
    jwks_url: str,
    issuer: str,
) -> dict[str, Any]:
    try:
        headers = jwt.get_unverified_header(token)
        kid = headers["kid"]
        public_key = get_public_key(jwks_url, kid)
        payload = jwt.decode(
            token,
            public_key=public_key,
            algorithms=["RS256"],
            audience="clerk",
            issuer=issuer,
        )
        return payload
    except jwt.exceptions.PyJWTError as e:
        logger.warning(f"Error decoding token: {e}")
        raise ValueError("Invalid Auth Token")
