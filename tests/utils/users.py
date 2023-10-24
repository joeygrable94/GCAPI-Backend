from os import environ
from typing import Dict

import requests

from app.core.config import settings


def get_auth0_access_token(
    email: str,
    password: str,
) -> Dict[str, str]:
    url = f"https://{settings.auth.domain}/oauth/token"
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": settings.auth.audience,
        "scope": "openid profile email",
    }
    clid: str | None = environ.get("AUTH0_SPA_CLIENT_ID", None)
    clsh: str | None = environ.get("AUTH0_SPA_CLIENT_SECRET", None)
    if clid is None:
        raise ValueError("AUTH0_SPA_CLIENT_ID is not set")
    if clsh is None:
        raise ValueError("AUTH0_SPA_CLIENT_SECRET is not set")
    headers = {"content-type": "application/json"}
    response = requests.post(url, json=data, headers=headers, auth=(clid, clsh))
    data = response.json()
    access_token = data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
