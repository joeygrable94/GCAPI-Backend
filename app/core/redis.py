import redis.asyncio as redis
from redis.asyncio.client import Redis

from app.core.config import settings  # pragma: no cover

redis_conn: Redis = redis.from_url(
    settings.redis.uri, decode_responses=True
)  # pragma: no cover
