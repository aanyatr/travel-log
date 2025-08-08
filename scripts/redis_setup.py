import asyncio
import aioredis
from app.config import REDIS_URL

async def redis_test():
    redis = await aioredis.from_url(REDIS_URL)
    await redis.set("test_key", "hello redis")
    value = await redis.get("test_key", encoding="utf-8")
    print(f"Redis test_key value: {value}")
    await redis.close()

if __name__ == "__main__":
    asyncio.run(redis_test())
