import json

from core.redis import get_redis_client


async def get_cache(key: str):
    redis_client = get_redis_client()
    data = await redis_client.get(key)

    await redis_client.aclose()

    if not data:
        return None

    return json.loads(data)


async def set_cache(key: str, data, expire: int = 300):
    redis_client = get_redis_client()

    if hasattr(data, "model_dump"):
        data = data.model_dump(mode="json")

    await redis_client.set(key, json.dumps(data), ex=expire)
    await redis_client.aclose()


async def delete_cache_pattern(pattern: str):
    redis_client = get_redis_client()
    keys = await redis_client.keys(pattern)

    if keys:
        await redis_client.delete(*keys)
