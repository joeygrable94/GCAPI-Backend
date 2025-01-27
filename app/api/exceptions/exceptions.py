from fastapi import status

from .errors import ErrorCode


# Generics
class ApiException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class InvalidID(ApiException):
    def __init__(self, message: str = ErrorCode.ID_INVALID):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message)


class MetricTypeInvalid(ApiException):
    def __init__(
        self,
        message: str = ErrorCode.METRIC_TYPE_INVALID,
        metric_info: str = "MetricType",
    ):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY, message + f": {metric_info}"
        )


class DomainInvalid(ApiException):
    def __init__(self, message: str = ErrorCode.DOMAIN_INVALID):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message)


class XmlInvalid(ApiException):
    def __init__(self, message: str = ErrorCode.XML_INVALID):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message)


# Users
class UserAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.USERNAME_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class UserNotFound(ApiException):
    def __init__(self, message: str = ErrorCode.USER_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Clients
class ClientAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.CLIENT_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class ClientNotFound(ApiException):
    def __init__(self, message: str = ErrorCode.CLIENT_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class ClientRelationshipNotFound(ApiException):
    def __init__(self, message: str = ErrorCode.CLIENT_RELATIONSHOP_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Entities
class EntityAlreadyExists(ApiException):
    def __init__(
        self, message: str = ErrorCode.ENTITY_EXISTS, entity_info: str = "DataModel"
    ):
        super().__init__(status.HTTP_400_BAD_REQUEST, message + f": {entity_info}")


class EntityNotFound(ApiException):
    def __init__(
        self, message: str = ErrorCode.ENTITY_NOT_FOUND, entity_info: str = "DataModel"
    ):
        super().__init__(status.HTTP_404_NOT_FOUND, message + f": {entity_info}")


class EntityRelationshipNotFound(ApiException):
    def __init__(
        self,
        message: str = ErrorCode.ENTITY_RELATIONSHOP_NOT_FOUND,
        entity_info: str = "DataModel",
    ):
        super().__init__(status.HTTP_400_BAD_REQUEST, message + f": {entity_info}")


class EntityQueryParamsInvalid(ApiException):
    def __init__(
        self,
        message: str = ErrorCode.ENTITY_QUERY_PARAMS_INVALID,
        entity_info: str = "DataModel",
    ):
        super().__init__(status.HTTP_400_BAD_REQUEST, message + f": {entity_info}")
