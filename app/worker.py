from typing import Any

from raven import Client
from asgi_correlation_id.context import correlation_id

from app.core.celery import celery_app
from app.core.config import settings


if not settings.DEBUG_MODE:  # pragma: no cover

    if settings.SENTRY_DSN:
        client_sentry: Client = Client(settings.SENTRY_DSN)

    @celery_app.before_task_publish.connect()
    def transfer_correlation_id(headers: Any) -> None:
        headers[settings.ASGI_ID_HEADER_KEY] = correlation_id.get()

    @celery_app.task_prerun.connect()
    def load_correlation_id(task: Any) -> None:
        id_value: Any = task.request.get(settings.ASGI_ID_HEADER_KEY)
        correlation_id.set(id_value)


@celery_app.task(acks_late=True)
def task_speak(word: str) -> str:
    return f"I say, {word}!"
