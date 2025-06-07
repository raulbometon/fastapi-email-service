# app/api/routes.py
from fastapi import APIRouter
from app.api.controllers import send_email
from app.api.models import EmailRequest


router = APIRouter()

@router.post('/send-email')
async def send_email_endpoint(req: EmailRequest):
    return await send_email(req)