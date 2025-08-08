# from fastapi import APIRouter, Request

# router = APIRouter()

# @router.post("/whatsapp/webhook")
# async def whatsapp_webhook(request: Request):
#     data = await request.json()
#     # TODO: Parse incoming WhatsApp messages
#     # Respond to WhatsApp if needed (200 OK)
#     return {"status": "received"}

# MEGHA CODE ABOVE 

# Twilio client + inbound webhook + routing
from fastapi import APIRouter, Request
from services.ai_client import generate_itinerary
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()


router = APIRouter()

# Twilio Client Config
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = 'whatsapp:+14155238886'
client = Client(account_sid, auth_token)

def send_whatsapp_message(to_number: str, message_text: str):
    """Send a WhatsApp message via Twilio."""
    message = client.messages.create(
        from_=twilio_number,
        body=message_text,
        to=f'whatsapp:{to_number}',
        status_callback="https://<your-ngrok-url>/whatsapp/status"
    )
    return message.sid

@router.post("/whatsapp/status")
async def whatsapp_status(request: Request):
    # Print the raw webhook request from Twilio
    print("---- STATUS CALLBACK RECEIVED ----")
    data = await request.form()
    print(dict(data))  # Log as dict for readability

    # Optionally extract key fields
    message_sid = data.get("MessageSid", "")
    message_status = data.get("MessageStatus", "")
    print(f"Message {message_sid} is now {message_status}")

    return {"status": "received"}

@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    # Debug: show the raw request body
    print("---- RAW TWILIO REQUEST BODY ----")
    raw_body = await request.body()
    print(raw_body)

    # Parse Twilio form data
    data = await request.form()
    print("---- PARSED TWILIO FORM DATA ----")
    print(dict(data))  # dict for easier reading

    # Extract fields from Twilio payload
    body = data.get("Body", "").strip()          # User's message text
    sender = data.get("From", "").replace("whatsapp:", "")  # Phone number
    message_id = data.get("SmsMessageSid", "")   # Unique message ID

    print(f"Incoming from {sender} (ID: {message_id}): {body}")

    # Basic AI parsing: expecting "Destination, Days, Preference"
    parts = body.split(",")
    if len(parts) == 3:
        destination, days, preferences = [p.strip() for p in parts]
        itinerary = generate_itinerary(destination, int(days), preferences)
        reply_text = "\n".join(
            f"Day {i['day']} ({i['date']}): {', '.join(i['activities'])}"
            for i in itinerary
        )
    else:
        reply_text = "Please send in format: Destination, Days, Preference"

    # Send response via Twilio
    send_whatsapp_message(sender, reply_text)

    # Acknowledge Twilio
    return {"status": "ok"}
