from fastapi import status

from app.core.exceptions import ApiException
from app.entities.website_sitemap.constants import ERROR_MESSAGE_XML_INVALID


class XmlInvalid(ApiException):
    def __init__(self, message: str = ERROR_MESSAGE_XML_INVALID):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message)
