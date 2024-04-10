from sentry_sdk import Client
from taskiq import InMemoryBroker, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

from app.api.monitoring import configure_monitoring
from app.core.config import settings
from app.core.utilities import get_uuid_str

sentry_client: Client | None = configure_monitoring()

task_broker: InMemoryBroker | ListQueueBroker = (
    ListQueueBroker(
        url=settings.worker.broker_url,
    )
    .with_result_backend(
        RedisAsyncResultBackend(
            redis_url=settings.worker.result_backend,
        )
    )
    .with_id_generator(get_uuid_str)
)

task_schedule_source = RedisScheduleSource(settings.worker.schedule_src)

task_scheduler: TaskiqScheduler = TaskiqScheduler(
    broker=task_broker,
    sources=[LabelScheduleSource(task_broker)],
)
