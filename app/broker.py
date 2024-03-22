from sentry_sdk import Client
from taskiq import InMemoryBroker
from taskiq_redis import PubSubBroker, RedisAsyncResultBackend

from app.api.monitoring import configure_monitoring
from app.core.config import settings
from app.core.utilities import get_uuid_str

sentry_client: Client | None = configure_monitoring()

broker: InMemoryBroker | PubSubBroker = (
    PubSubBroker(
        url=settings.worker.broker_url,
    )
    .with_result_backend(
        RedisAsyncResultBackend(
            redis_url=settings.worker.result_backend,
        )
    )
    .with_id_generator(get_uuid_str)
)
