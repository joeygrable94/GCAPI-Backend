from enum import Enum
from typing import Dict, Union

from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: Union[str, Dict[str, str]]


class ErrorCodeReasonModel(BaseModel):
    code: str
    reason: str


class ErrorCode(str, Enum):
    # authorization
    UNAUTHORIZED = "UNAUTHORIZED"
    # generics
    INVALID_ID = "INVALID_ID"
    # users
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_EXISTS = "USER_EXISTS"
    # clients
    CLIENT_NOT_FOUND = "CLIENT_NOT_FOUND"
    CLIENT_EXISTS = "CLIENT_EXISTS"
    # notes
    NOTE_NOT_FOUND = "NOTE_NOT_FOUND"
    NOTE_EXISTS = "NOTE_EXISTS"
    # websites
    WEBSITE_NOT_FOUND = "WEBSITE_NOT_FOUND"
    WEBSITE_DOMAIN_INVALID = "WEBSITE_DOMAIN_INVALID"
    WEBSITE_DOMAIN_EXISTS = "WEBSITE_DOMAIN_EXISTS"
    # sitemaps
    WEBSITE_MAP_NOT_FOUND = "WEBSITE_MAP_NOT_FOUND"
    WEBSITE_MAP_EXISTS = "WEBSITE_MAP_EXISTS"
    WEBSITE_MAP_UNASSIGNED_WEBSITE_ID = "WEBSITE_MAP_UNASSIGNED_WEBSITE_ID"
    # webpages
    WEBSITE_PAGE_NOT_FOUND = "WEBSITE_PAGE_NOT_FOUND"
    WEBSITE_PAGE_URL_EXISTS = "WEBSITE_PAGE_URL_EXISTS"
    WEBSITE_PAGE_UNASSIGNED_WEBSITE_ID = "WEBSITE_PAGE_UNASSIGNED_WEBSITE_ID"
    # web page speed insights
    WEBSITE_PAGE_SPEED_INSIGHTS_EXISTS = "WEBSITE_PAGE_SPEED_INSIGHTS_EXISTS"
    WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND = "WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND"
