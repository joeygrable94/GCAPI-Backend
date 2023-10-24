from typing import Any, Union

from fastapi import Request, WebSocket
from redis.asyncio.client import Redis


def default_identifier(request: Union[Request, WebSocket]) -> str:
    ip: str
    forwarded: str | None = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0]
    elif request.client:
        ip = request.client.host
    else:
        ip = "127.0.0.1"
    return ip + ":" + request.scope["path"]


class FastAPILimiter:
    redis: Redis
    prefix: str | None = None
    lua_sha: str | None = None
    lua_script: str = """local key = KEYS[1]
local limit = tonumber(ARGV[1])
local expire_time = ARGV[2]

local current = tonumber(redis.call('get', key) or "0")
if current > 0 then
 if current + 1 > limit then
 return redis.call("PTTL",key)
 else
        redis.call("INCR", key)
 return 0
 end
else
    redis.call("SET", key, 1,"px",expire_time)
 return 0
end"""

    @classmethod
    async def init(
        cls: Any,
        redis: Redis,
        prefix: str = "fastapi-limiter",
    ) -> None:
        cls.redis = redis
        cls.prefix = prefix
        cls.lua_sha = await redis.script_load(cls.lua_script)

    @classmethod
    async def close(cls: Any) -> None:
        await cls.redis.aclose()
