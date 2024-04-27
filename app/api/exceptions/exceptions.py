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


# Users
class UserAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.USERNAME_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class UserNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.USER_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Clients
class ClientAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.CLIENT_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class ClientNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.CLIENT_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class ClientRelationshipNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.CLIENT_RELATIONSHOP_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Notes
class NoteAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.NOTE_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class NoteNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.NOTE_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Sharpspring
class SharpspringAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.SHARPSPRING_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class SharpspringNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.SHARPSPRING_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Ga4 Property
class Ga4PropertyAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.GA4_PROPERTY_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class Ga4PropertyNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.GA4_PROPERTY_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Websites
class WebsiteAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_DOMAIN_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class WebsiteNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class WebsiteDomainInvalid(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_DOMAIN_INVALID):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


# Website Sitemaps
class WebsiteMapAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_MAP_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class WebsiteMapNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_MAP_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class WebsiteMapUrlXmlInvalid(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_MAP_URL_XML_INVALID):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


# Website Pages
class WebsitePageAlreadyExists(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_PAGE_URL_EXISTS):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class WebsitePageNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_PAGE_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Website Page Speed Insights
class WebsitePageSpeedInsightsNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_PAGE_SPEED_INSIGHTS_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


# Website Keyword Corpus
class WebsitePageKeywordCorpusNotExists(ApiException):
    def __init__(self, message: str = ErrorCode.WEBSITE_PAGE_KEYWORD_CORPUS_NOT_FOUND):
        super().__init__(status.HTTP_404_NOT_FOUND, message)
