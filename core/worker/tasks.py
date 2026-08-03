import asyncio

from core.email import send_verification_email
from core.worker.celery import celery


@celery.task
def send_verification_email_task(email: str, token: str):

    asyncio.run(send_verification_email(email, token))
