import asyncio

from core.email import send_password_reset_email, send_verification_email
from core.worker.celery import celery


@celery.task
def send_verification_email_task(email: str, token: str):

    asyncio.run(send_verification_email(email, token))


@celery.task
def send_password_reset_email_task(email: str, token: str):

    asyncio.run(send_password_reset_email(email, token))
