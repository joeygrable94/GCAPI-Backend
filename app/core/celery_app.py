from celery import Celery
from app.core.config import settings

# init worker
celery_app = Celery('worker')
celery_app.conf.broker_url = settings.C_BROKER_URI
celery_app.conf.result_backend = settings.C_BACKEND_URI

# load celery tasks
celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue"
}
