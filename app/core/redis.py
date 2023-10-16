import redis.asyncio  # pragma: no cover

from app.core.config import settings  # pragma: no cover

redis_conn = redis.asyncio.from_url(
    settings.redis.uri, decode_responses=True
)  # pragma: no cover
