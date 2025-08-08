import aioredis
from app.config import REDIS_URL

redis = None

async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(REDIS_URL)
    return redis
