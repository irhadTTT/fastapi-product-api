
import json

from core.logging import logger
from core.redis import get_redis_client


async def get_cache(key: str):
    redis_client = get_redis_client()

    try:
        data = await redis_client.get(key)

        if not data:
            return None

        return json.loads(data)

    except Exception as exc:
        logger.warning("Cache read failed; continuing without cache: %s", exc)
        return None

    finally:
        await redis_client.aclose()


async def set_cache(key: str, data, expire: int = 300):
    redis_client = get_redis_client()

    try:
        if hasattr(data, "model_dump"):
            data = data.model_dump(mode="json")

        await redis_client.set(key, json.dumps(data), ex=expire)

    except Exception as exc:
        logger.warning("Cache write failed; continuing without cache: %s", exc)

    finally:
        await redis_client.aclose()


async def delete_cache_pattern(pattern: str):
    redis_client = get_redis_client()

    try:
        keys = await redis_client.keys(pattern)

        if keys:
            await redis_client.delete(*keys)

    except Exception as exc:
        logger.warning("Cache invalidation failed: %s", exc)

    finally:
        await redis_client.aclose()