from fastapi import status

from app.core.exceptions import ApiException
from app.entities.core_organization.constants import (
    ERROR_MESSAGE_ORGANIZATION_EXISTS,
    ERROR_MESSAGE_ORGANIZATION_NOT_FOUND,
    ERROR_MESSAGE_ORGANIZATION_RELATIONSHOP_NOT_FOUND,
)


class OrganizationAlreadyExists(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_ORGANIZATION_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class OrganizationNotFound(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_ORGANIZATION_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class OrganizationRelationshipNotFound(ApiException):
    def __init__(
        self, message: str = ERROR_MESSAGE_ORGANIZATION_RELATIONSHOP_NOT_FOUND
    ):
        super().__init__(status.HTTP_404_NOT_FOUND, message)
