import redis.asyncio as redis  # pragma: no cover
from redis.asyncio.client import Redis  # pragma: no cover

from app.core.config import settings  # pragma: no cover

redis_conn: Redis = redis.from_url(
    settings.redis.uri, decode_responses=True
)  # pragma: no cover
