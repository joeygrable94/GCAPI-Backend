from typing import List

from app.core.config import settings

from .console import Logger

logger: Logger = Logger(name=settings.api.logger_name, level=settings.api.logging_level)

__all__: List[str] = [
    "logger",
]
