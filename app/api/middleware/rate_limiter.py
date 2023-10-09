from app.core.redis import redis_conn
from app.schemas import RateLimitedToken


async def limiter(key: str, limit: int, expires: int = 60) -> RateLimitedToken:
    redis_key = "iplimit:" + key
    req = await redis_conn.incr(redis_key)
    if req == 1:
        await redis_conn.expire(redis_key, expires)
        ttl = expires
    else:
        ttl = await redis_conn.ttl(redis_key)
    if req > limit:
        return RateLimitedToken(call=False, ttl=ttl)
    else:
        return RateLimitedToken(call=True, ttl=ttl)
