import logging

from app.core.config import ApiModes, settings

LOGGER_NAME = LOGGER_NAME = (
    f"{settings.api.logger_name}_test"
    if settings.api.mode == ApiModes.test.value
    else settings.api.logger_name
)


logger: logging.Logger = logging.getLogger(LOGGER_NAME)
logger.setLevel("DEBUG")

log_file_handler: logging.FileHandler = logging.FileHandler(f"{LOGGER_NAME}.log")
log_file_frmt: logging.Formatter = logging.Formatter(
    "%(levelname)-11s\b%(asctime)s %(name)s:%(lineno)d %(message)s"
)
log_file_handler.setFormatter(log_file_frmt)
logger.addHandler(log_file_handler)

log_stream_handler: logging.StreamHandler = logging.StreamHandler()
log_stream_frmt: logging.Formatter = logging.Formatter(
    "%(levelname)-11s\b%(asctime)-6s %(name)s:%(lineno)d %(message)s"
)
log_stream_handler.setFormatter(log_stream_frmt)
logger.addHandler(log_stream_handler)

__all__: list[str] = [
    "logger",
]
