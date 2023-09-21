from typing import Any

from app.schemas.client import ClientACL
from app.schemas.client_website import ClientWebsiteACL
from app.schemas.website import WebsiteACL


def test_client_acl() -> Any:
    assert len(ClientACL.__acl__) > 0  # type: ignore


def test_client_website_acl() -> Any:
    assert len(ClientWebsiteACL.__acl__) > 0  # type: ignore


def test_website_acl() -> Any:
    assert len(WebsiteACL.__acl__) > 0  # type: ignore
