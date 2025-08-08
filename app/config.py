import os
from dotenv import load_dotenv

# Load .env file variables automatically
load_dotenv()

# MongoDB connection URI (e.g., mongodb://localhost:27017)
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Redis connection URL (e.g., redis://localhost:6379)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# WhatsApp API config
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "")
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "")

# OpenAI or other LLM API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Payment gateway API key (mock or real)
PAYMENT_GATEWAY_API_KEY = os.getenv("PAYMENT_GATEWAY_API_KEY", "")