import base64
import json
from os import environ

import requests

from app.core.config import settings


def get_auth0_access_token_value(
    email: str,
    password: str,
    audience: str = settings.auth.audience,
    scopes: str = "openid profile email",
) -> str:
    url = f"https://{settings.auth.domain}/oauth/token"
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": audience,
        "scope": scopes,
    }
    clid: str | None = environ.get("AUTH_SPA_CLIENT_ID", None)
    clsh: str | None = environ.get("AUTH_SPA_CLIENT_SECRET", None)
    if clid is None:
        raise ValueError("AUTH_SPA_CLIENT_ID is not set")
    if clsh is None:
        raise ValueError("AUTH_SPA_CLIENT_SECRET is not set")
    headers = {"content-type": "application/json"}
    response = requests.post(url, json=data, headers=headers, auth=(clid, clsh))
    data = response.json()
    access_token = data["access_token"]
    return access_token


def get_auth0_access_token(
    email: str,
    password: str,
) -> dict[str, str]:
    access_token = get_auth0_access_token_value(email=email, password=password)
    return {"Authorization": f"Bearer {access_token}"}


def get_malformed_token(token: str) -> str:
    payload_encoded = token.split(".")[1]
    payload_str = base64.b64decode(f"{payload_encoded}==").decode()
    payload = json.loads(payload_str)

    payload["sub"] = "evil"
    bad_payload_str = json.dumps(payload, separators=(",", ":"))
    bad_payload_encoded = (
        base64.b64encode(bad_payload_str.encode()).decode().replace("=", "")
    )

    return token.replace(payload_encoded, bad_payload_encoded)


def get_missing_kid_token(token: str) -> str:
    header_encoded = token.split(".")[0]
    header_str = base64.b64decode(f"{header_encoded}==").decode()
    header = json.loads(header_str)

    header.pop("kid")
    bad_header_str = json.dumps(header, separators=(",", ":"))
    bad_header_encoded = (
        base64.b64encode(bad_header_str.encode()).decode().replace("=", "")
    )

    return token.replace(header_encoded, bad_header_encoded)


def get_invalid_token(token: str) -> str:
    header = token.split(".")[0]
    return token.replace(header, header[:-3])
