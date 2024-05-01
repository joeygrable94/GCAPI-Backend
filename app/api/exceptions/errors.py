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
    UNVERIFIED_ACCESS_DENIED = "UNVERIFIED_ACCESS_DENIED"
    INSUFFICIENT_PERMISSIONS = "INSUFFICIENT_PERMISSIONS"
    INSUFFICIENT_PERMISSIONS_ACCESS = (
        "You do not have permission to access this resource"
    )
    INSUFFICIENT_PERMISSIONS_ACTION = (
        "You do not have permission to take this action on this resource"
    )
    INSUFFICIENT_PERMISSIONS_RESPONSE = (
        "You do not have permission to access the output of this resource"
    )
    INSUFFICIENT_PERMISSIONS_PAGINATION = (
        "You do not have permission to access the paginated output of this resource"
    )
    INSUFFICIENT_PERMISSIONS_SCOPE_ADD = (
        "You do not have permission to add role based access to users"
    )
    INSUFFICIENT_PERMISSIONS_SCOPE_REMOVE = (
        "You do not have permission to remove role based access to users"
    )
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
    # bdx feeds
    BDX_FEED_EXISTS = "BDX_FEED_EXISTS"
    BDX_FEED_NOT_FOUND = "BDX_FEED_NOT_FOUND"
    # sharpspring
    SHARPSPRING_EXISTS = "SHARPSPRING_EXISTS"
    SHARPSPRING_NOT_FOUND = "SHARPSPRING_NOT_FOUND"
    # google cloud
    GO_CLOUD_EXISTS = "GO_CLOUD_EXISTS"
    GO_CLOUD_NOT_FOUND = "GO_CLOUD_NOT_FOUND"
    # google analytics
    GA4_PROPERTY_EXISTS = "GA4_PROPERTY_EXISTS"
    GA4_PROPERTY_NOT_FOUND = "GA4_PROPERTY_NOT_FOUND"
    GA4_STREAM_EXISTS = "GA4_STREAM_EXISTS"
    GA4_STREAM_NOT_FOUND = "GA4_STREAM_NOT_FOUND"
    # google search console
    GO_SEARCH_PROPERTY_EXISTS = "GO_SEARCH_PROPERTY_EXISTS"
    GO_SEARCH_PROPERTY_NOT_FOUND = "GO_SEARCH_PROPERTY_NOT_FOUND"
    GO_SEARCH_METRIC_TYPE_INVALID = "Input should be 'searchappearance', 'query', 'page', 'device' or 'country'"  # noqa: E501, E261
    GO_SEARCH_METRIC_NOT_FOUND = "GO_SEARCH_METRIC_NOT_FOUND"
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
