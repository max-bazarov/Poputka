from pydantic import EmailStr

from app.auth.email import send_email
from app.tasks.celery import celery


@celery.task
async def send_verification_email(
    user_email: EmailStr, user_name: str, user_id: int
):
    await send_email(user_email=user_email, user_name=user_name, user_id=user_id)
