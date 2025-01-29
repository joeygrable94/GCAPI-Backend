from enum import Enum
from typing import Union

from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: Union[str, dict[str, str]]


class ErrorCodeReasonModel(BaseModel):
    code: str
    reason: str


class ErrorCode(str, Enum):
    # generics
    ID_INVALID = "ID_INVALID"
    ID_NOT_PROVIDED = "ID_NOT_PROVIDED"
    DOMAIN_INVALID = "DOMAIN_INVALID"
    XML_INVALID = "XML_INVALID"
    INPUT_SCHEMA_INVALID = "SCHEMA_INVALID"
    METRIC_TYPE_INVALID = "METRIC_TYPE_INVALID"
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
    # entities
    ENTITY_EXISTS = "ENTITY_EXISTS"
    ENTITY_NOT_FOUND = "ENTITY_NOT_FOUND"
    ENTITY_RELATIONSHOP_NOT_FOUND = "ENTITY_RELATIONSHOP_NOT_FOUND"
    ENTITY_QUERY_PARAMS_INVALID = "ENTITY_QUERY_PARAMS_INVALID"
