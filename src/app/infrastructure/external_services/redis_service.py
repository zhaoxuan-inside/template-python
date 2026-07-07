from typing import Optional

import redis.asyncio as aioredis

from app.infrastructure.config.settings import settings


class RedisService:
    _instance: Optional["RedisService"] = None

    def __init__(self) -> None:
        self._client: Optional[aioredis.Redis] = None

    async def connect(self) -> None:
        if not self._client:
            self._client = aioredis.from_url(settings.redis_url)
            await self._client.ping()

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None

    async def get(self, key: str) -> Optional[str]:
        if not self._client:
            await self.connect()
        return await self._client.get(key)

    async def set(self, key: str, value: str, expire: Optional[int] = None) -> None:
        if not self._client:
            await self.connect()
        await self._client.set(key, value, ex=expire)

    async def delete(self, key: str) -> None:
        if not self._client:
            await self.connect()
        await self._client.delete(key)
