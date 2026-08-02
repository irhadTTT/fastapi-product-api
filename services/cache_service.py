import json

from core.redis import redis_client


async def get_cache(key: str):
    data = await redis_client.get(key)

    if not data:
        return None

    return json.loads(data)


async def set_cache(key: str, data, expire: int = 300):
    if hasattr(data, "model_dump"):
        data = data.model_dump(mode="json")

    await redis_client.set(key, json.dumps(data), ex=expire)


async def delete_cache_pattern(pattern: str):
    keys = await redis_client.keys(pattern)

    if keys:
        await redis_client.delete(*keys)
