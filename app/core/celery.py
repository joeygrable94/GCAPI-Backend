from typing import Any

from celery import Celery  # type: ignore

from app.core.config import settings

# init worker
celery_app: Any = Celery("worker")
celery_app.conf.update(
    broker_url=f"{settings.REDIS_CONN_URI}{settings.CELERY_WORKER_BROKER}",
    result_backend=f"{settings.REDIS_CONN_URI}{settings.CELERY_WORKER_BACKEND}",
    task_track_started=True,
    task_serializer='pickle',
    result_serializer='pickle',
    accept_content=['pickle', 'json'],
    result_expires=200,
    result_persistent=True,
    worker_send_task_events=False,
    worker_prefetch_multiplier=1,
)

# load celery tasks
celery_app.conf.task_routes = {
    "app.worker.task_speak": settings.CELERY_WORKER_TASK_QUEUE,
    "app.worker.task_website_sitemap_fetch_pages": settings.CELERY_WORKER_TASK_QUEUE,
    "app.worker.task_website_sitemap_process_pages": settings.CELERY_WORKER_TASK_QUEUE,
    "app.worker.task_website_page_pagespeedinsights_fetch": settings.CELERY_WORKER_TASK_QUEUE,  # noqa: E501
}
