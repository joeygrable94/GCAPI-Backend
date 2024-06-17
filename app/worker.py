from taskiq import AsyncBroker, AsyncResultBackend, ScheduleSource, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

from app.core.config import settings

task_broker_results: AsyncResultBackend = RedisAsyncResultBackend(
    redis_url=settings.worker.result_backend,
    result_ex_time=settings.worker.result_ex_time,
)

task_broker: AsyncBroker = ListQueueBroker(
    url=settings.worker.broker_url,
).with_result_backend(task_broker_results)

task_schedule_source: ScheduleSource = RedisScheduleSource(
    settings.worker.schedule_src
)  # pragma: no cover

task_scheduler: TaskiqScheduler = TaskiqScheduler(  # pragma: no cover
    broker=task_broker,
    sources=[LabelScheduleSource(task_broker)],
)
