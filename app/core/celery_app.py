from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=f"{settings.REDIS_CONN_URI}{settings.CELERY_WORKER_BROKER}"
)

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
