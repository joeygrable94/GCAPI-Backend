from enum import Enum
from typing import Dict, Union

from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: Union[str, Dict[str, str]]


class ErrorCodeReasonModel(BaseModel):
    code: str
    reason: str


class ErrorCode(str, Enum):
    # generics
    ID_INVALID = "ID_INVALID"
    ID_NOT_PROVIDED = "ID_NOT_PROVIDED"
    # authorization
    UNAUTHORIZED = "UNAUTHORIZED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    UNVERIFIED_ACCESS_DENIED = "UNVERIFIED_ACCESS_DENIED"
    # security
    IP_RESTRICTED_TOO_MANY_REQUESTS = "call limit reached"
    # users
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USERNAME_EXISTS = "USERNAME_EXISTS"
    # clients
    CLIENT_NOT_FOUND = "CLIENT_NOT_FOUND"
    CLIENT_EXISTS = "CLIENT_EXISTS"
    CLIENT_RELATIONSHOP_NOT_FOUND = "CLIENT_RELATIONSHOP_NOT_FOUND"
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
    WEBSITE_MAP_URL_XML_INVALID = "WEBSITE_MAP_URL_XML_INVALID"
    # webpages
    WEBSITE_PAGE_NOT_FOUND = "WEBSITE_PAGE_NOT_FOUND"
    WEBSITE_PAGE_URL_EXISTS = "WEBSITE_PAGE_URL_EXISTS"
    # web page speed insights
    WEBSITE_PAGE_SPEED_INSIGHTS_EXISTS = "WEBSITE_PAGE_SPEED_INSIGHTS_EXISTS"
    WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND = "WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND"
    # web page keyword corpus
    WEBSITE_PAGE_KEYWORD_CORPUS_EXISTS = "WEBSITE_PAGE_KEYWORD_CORPUS_EXISTS"
    WEBSITE_PAGE_KEYWORD_CORPUS_NOT_FOUND = "WEBSITE_PAGE_KEYWORD_CORPUS_NOT_FOUND"
