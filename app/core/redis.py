import redis.asyncio

from app.core.config import settings

redis_conn = redis.asyncio.from_url(settings.REDIS_CONN_URI, decode_responses=True)
