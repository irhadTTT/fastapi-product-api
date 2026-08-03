from time import perf_counter

from fastapi import Request

from core.logging import logger


async def log_requests(request: Request, call_next):

    start = perf_counter()

    response = await call_next(request)

    duration = perf_counter() - start

    logger.info(
        "%s %s -> %s (%.3fs)",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response
