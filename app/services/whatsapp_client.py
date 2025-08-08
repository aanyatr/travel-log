from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    # TODO: Parse incoming WhatsApp messages
    # Respond to WhatsApp if needed (200 OK)
    return {"status": "received"}
