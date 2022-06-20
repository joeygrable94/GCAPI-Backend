from app.core.config import settings

from .console import Logger

logger = Logger(name=settings.LOGGER_NAME, level=settings.LOGGING_LEVEL)
