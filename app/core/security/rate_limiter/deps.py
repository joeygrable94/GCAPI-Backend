from math import ceil
from typing import Annotated, Any

import redis as pyredis
from fastapi import Request, Response
from pydantic import Field

from app.core.logger import logger

from .core import FastAPILimiter, default_identifier
from .exceptions import RateLimitedRequestException


class RateLimiter:
    def __init__(
        self,
        times: Annotated[int, Field(strict=True, ge=0)] = 1,
        milliseconds: Annotated[int, Field(strict=True, ge=-1)] = 0,
        seconds: Annotated[int, Field(strict=True, ge=-1)] = 0,
        minutes: Annotated[int, Field(strict=True, ge=-1)] = 0,
        hours: Annotated[int, Field(strict=True, ge=-1)] = 0,
    ):
        self.times = times
        self.milliseconds = (
            milliseconds + 1000 * seconds + 60000 * minutes + 3600000 * hours
        )

    async def _check(self: Any, key: str) -> int:
        redis = FastAPILimiter.redis
        pexpire = await redis.evalsha(
            FastAPILimiter.lua_sha, 1, key, str(self.times), str(self.milliseconds)
        )
        return pexpire

    async def __call__(self, request: Request, response: Response) -> None:
        if not FastAPILimiter.redis:  # pragma: no cover
            raise Exception(
                "You must call FastAPILimiter.init in startup event of fastapi!"
            )
        route_index = 0
        dep_index = 0
        for i, route in enumerate(request.app.routes):
            if route.path == request.scope["path"] and request.method in route.methods:
                route_index = i
                for j, dependency in enumerate(route.dependencies):
                    if self is dependency.dependency:
                        dep_index = j
                        break

        # moved here because constructor run before app startup
        rate_key = default_identifier(request)
        key = f"{FastAPILimiter.prefix}:{rate_key}:{route_index}:{dep_index}"
        try:
            pexpire = await self._check(key)
        except pyredis.exceptions.NoScriptError:  # pragma: no cover
            FastAPILimiter.lua_sha = await FastAPILimiter.redis.script_load(
                FastAPILimiter.lua_script
            )
            pexpire = await self._check(key)
        if pexpire != 0:
            expire = ceil(pexpire / 1000)
            logger.warning(f"Rate limit exceeded for {key}, expires {expire}.")
            raise RateLimitedRequestException(expire=expire)


"""
class WebSocketRateLimiter(RateLimiter):
    async def __call__(self, ws: WebSocket, context_key: str = "") -> None:  # type: ignore  # noqa: E501
        assert type(ws) is WebSocket
        if not FastAPILimiter.redis:
            raise Exception(
                "You must call FastAPILimiter.init in startup event of fastapi!"
            )
        rate_key = default_identifier(ws)
        key = f"{FastAPILimiter.prefix}:ws:{rate_key}:{context_key}"
        pexpire = await self._check(key)
        if pexpire != 0:
            expire = ceil(pexpire / 1000)
            logger.warning(f"Rate limit exceeded for {key}, expires {expire}.")
            raise RateLimitedRequestException(expire=expire)
"""
