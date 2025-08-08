from fastapi import FastAPI
from app.utils.webhook_handler import router as whatsapp_router

app = FastAPI()
app.include_router(whatsapp_router)

@app.get("/")
def health_check():
    return {"status": "running"}