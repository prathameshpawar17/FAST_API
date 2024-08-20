from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.sms_gateway import sms_gateway

router = APIRouter()

class SMSMessage(BaseModel):
    sender: str
    receiver: str
    content: str

@router.post("/send_sms")
async def send_sms(message: SMSMessage):
    success = await sms_gateway.send_sms(message.sender, message.receiver, message.content)
    if success:
        return {"message": "SMS sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send SMS")

@router.get("/inbox/{phone_number}")
async def get_inbox(phone_number: str):
    messages = sms_gateway.get_inbox(phone_number)
    return {"inbox": messages}