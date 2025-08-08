<<<<<<< Updated upstream
=======
# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    form_data = await request.form()  # Twilio sends application/x-www-form-urlencoded
    print("📩 Incoming WhatsApp Message:")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    
    # Respond to Twilio (must be 200 OK)
    return PlainTextResponse("Message received", status_code=200)

@app.post("/whatsapp/status")
async def whatsapp_status(request: Request):
    form_data = await request.form()
    print("\n📡 Status Callback Received:")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    return "OK"
>>>>>>> Stashed changes
