from fastapi import status

from app.core.exceptions import ApiException
from app.entities.website.constants import ERROR_MESSAGE_DOMAIN_INVALID


class DomainInvalid(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_DOMAIN_INVALID):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message)
