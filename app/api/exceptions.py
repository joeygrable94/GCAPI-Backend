# Generics
class EntityException(Exception):
    pass


class EntityAlreadyExists(EntityException):
    pass


class EntityNotExists(EntityException):
    pass


class InvalidID(EntityException):
    pass


class EntityIdNotProvided(EntityException):
    pass


class EntityValueRequired(Exception):
    pass


# Users
class UserException(EntityException):
    pass


class UserAlreadyExists(UserException):
    pass


class UserNotExists(UserException):
    pass


# Clients
class ClientsException(EntityException):
    pass


class ClientAlreadyExists(ClientsException):
    pass


class ClientNotExists(ClientsException):
    pass


# Notes
class NoteException(EntityException):
    pass


class NoteAlreadyExists(NoteException):
    pass


class NoteNotExists(NoteException):
    pass


# Websites
class WebsitesException(EntityException):
    pass


class WebsiteAlreadyExists(WebsitesException):
    pass


class WebsiteNotExists(WebsitesException):
    pass


class WebsiteDomainInvalid(WebsitesException):
    pass


# Website Sitemaps
class WebsiteMapAlreadyExists(WebsitesException):
    pass


class WebsiteMapNotExists(WebsitesException):
    pass


# Website Pages
class WebsitePageAlreadyExists(WebsitesException):
    pass


class WebsitePageNotExists(WebsitesException):
    pass


# Website Page Speed Insights
class WebsitePageSpeedInsightsAlreadyExists(WebsitesException):
    pass


class WebsitePageSpeedInsightsNotExists(WebsitesException):
    pass
