from fastapi import APIRouter, Request, HTTPException
import logging
from app.utils.helpers import user_session_key, create_user_session_data
import redis
import re
import requests
import os

router = APIRouter()
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

TWILIO_API_URL = "https://api.twilio.com/2010-04-01/Accounts"
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

def send_whatsapp_message(to: str, body: str):
    """Send outbound WhatsApp message via Twilio API."""
    try:
        url = f"{TWILIO_API_URL}/{TWILIO_SID}/Messages.json"
        data = {
            "From": f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
            "To": f"whatsapp:{to}",
            "Body": body
        }
        resp = requests.post(url, data=data, auth=(TWILIO_SID, TWILIO_AUTH_TOKEN))
        resp.raise_for_status()
        logging.info(f"Sent message to {to}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")


@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    """Receive incoming WhatsApp messages from Twilio."""
    try:
        form_data = await request.form()
        sender = form_data.get("From", "").replace("whatsapp:", "")
        message_text = form_data.get("Body", "").strip()
        message_id = form_data.get("MessageSid")

        logging.info(f"Incoming from {sender}: {message_text} (ID: {message_id})")

        # Save session data in Redis
        session_key = user_session_key(sender)
        r.hset(session_key, mapping=create_user_session_data(current_intent="processing"))

        # Route request
        if re.search(r"\bhelp\b", message_text, re.IGNORECASE):
            send_whatsapp_message(sender, "Here are some commands you can use: ...")
        elif re.search(r"\btrack\b", message_text, re.IGNORECASE):
            send_whatsapp_message(sender, "Tracking your request...")
        else:
            send_whatsapp_message(sender, "Sorry, I didn't understand. Type 'help'.")

        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")