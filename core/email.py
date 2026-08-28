from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic_settings import BaseSettings

from core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)


async def send_verification_email(email: str, token: str):

    if settings.TESTING:
        return

    link = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    message = MessageSchema(
        subject="Verify your StockFlow account",
        recipients=[email],
        body=f"""
        <html>
            <body>
                <h2>Welcome to StockFlow</h2>

                <p>
                    Thanks for creating your account.
                    Please verify your email address.
                </p>

                <p>
                    Click the button below to verify your email address:
                </p>

                <p>
                    <a href="{link}"
                    style="background:#2563eb;color:#fff;padding:12px 20px;
                            text-decoration:none;border-radius:6px;display:inline-block;">
                        Verify Email
                    </a>
                </p>

                <p>
                    If you did not create this account,
                    you can ignore this email.
                </p>

                <br>

                <p>
                    Kind regards,<br>
                    StockFlow Team
                </p>
            </body>
        </html>
        """,
        subtype="html",
    )

    fm = FastMail(conf)

    await fm.send_message(message)


async def send_password_reset_email(email: str, token: str):

    if settings.TESTING:
        return

    link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    message = MessageSchema(
        subject="Reset your StockFlow password",
        recipients=[email],
        body=f"""
        <html>
            <body>
                <h2>Password Reset</h2>

                <p>
                    We received a request to reset your StockFlow password.
                </p>

                <p>
                    Click the button below to set a new password:
                </p>

                <p>
                    <a href="{link}"
                    style="background:#2563eb;color:#fff;padding:12px 20px;
                            text-decoration:none;border-radius:6px;display:inline-block;">
                        Reset Password
                    </a>
                </p>

                <p>
                    This link will expire in 30 minutes.
                </p>

                <p>
                    If you did not request a password reset,
                    you can ignore this email.
                </p>

                <br>

                <p>
                    Kind regards,<br>
                    StockFlow Team
                </p>
            </body>
        </html>
        """,
        subtype="html",
    )

    fm = FastMail(conf)

    await fm.send_message(message)
