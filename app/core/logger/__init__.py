from typing import List

from app.core.config import ApiModes, settings

from .console import Logger

LOGGER_NAME = LOGGER_NAME = (
    f"{settings.api.logger_name}_test"
    if settings.api.mode == ApiModes.test
    else settings.api.logger_name
)
logger: Logger = Logger(name=LOGGER_NAME, level=settings.api.logging_level)

__all__: List[str] = [
    "logger",
]
