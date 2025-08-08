import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URI

async def init_db():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.travel_mcp

    # Ensure unique index on user phone
    await db.users.create_index("phone", unique=True)
    print("Created unique index on users.phone")

    # Ensure index on trips.ownerPhone
    await db.trips.create_index("ownerPhone")
    print("Created index on trips.ownerPhone")

    # Ensure index on bookings.tripId
    await db.bookings.create_index("tripId")
    print("Created index on bookings.tripId")

    # Additional indexes can be added here...

    print("MongoDB initialization complete.")
    client.close()


if __name__ == "__main__":
    asyncio.run(init_db())
