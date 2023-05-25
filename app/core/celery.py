from os import environ
from typing import Any, Dict

from celery import Celery  # type: ignore
from kombu import Queue  # type: ignore


# dynamic routing
def route_task(
    name: str, args: Any, kwargs: Any, options: Any, task: Any = None, **kw: Any
) -> Dict[str, Any]:
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "tasks"}


# init worker app
def create_celery_worker(name: str = "worker") -> Celery:
    worker: Celery = Celery(name)
    worker.conf.update(
        broker_url=environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    )
    worker.conf.update(
        result_backend=environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    )
    worker.conf.update(task_track_started=True)
    worker.conf.update(task_serializer="pickle")
    worker.conf.update(result_serializer="pickle")
    worker.conf.update(accept_content=["pickle", "json"])
    worker.conf.update(result_expires=200)
    worker.conf.update(result_persistent=True)
    worker.conf.update(worker_send_task_events=False)
    worker.conf.update(worker_prefetch_multiplier=1)
    worker.conf.update(
        task_queues=(
            Queue("tasks"),
            Queue("websites"),
            Queue("sitemaps"),
            Queue("webpages"),
        )
    )
    worker.conf.update(task_routes=(route_task,))

    return worker
