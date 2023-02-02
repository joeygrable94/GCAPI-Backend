from typing import Any

from app.db.schemas.accesstoken import AccessTokenACL
from app.db.schemas.client import ClientACL
from app.db.schemas.client_website import ClientWebsiteACL
from app.db.schemas.ipaddress import IpAddressACL
from app.db.schemas.user_client import UserClientACL
from app.db.schemas.website import WebsiteACL


def test_ipaddress_acl() -> Any:
    assert len(IpAddressACL.__acl__(IpAddressACL)) > 0  # type: ignore


def test_client_acl() -> Any:
    assert len(ClientACL.__acl__(ClientACL)) > 0  # type: ignore


def test_client_website_acl() -> Any:
    assert len(ClientWebsiteACL.__acl__(ClientWebsiteACL)) > 0  # type: ignore


def test_token_acl() -> Any:
    assert len(AccessTokenACL.__acl__(AccessTokenACL)) > 0  # type: ignore


def test_user_client_acl() -> Any:
    assert len(UserClientACL.__acl__(UserClientACL)) > 0  # type: ignore


def test_website_acl() -> Any:
    assert len(WebsiteACL.__acl__(WebsiteACL)) > 0  # type: ignore
