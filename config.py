from motor.motor_asyncio import AsyncIOMotorClient
import os

client: AsyncIOMotorClient | None = None
_database = None

def connect_to_mongo():
    global client, _database
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
    _database = client["ecommerce_db"]

def close_mongo_connection():
    global client
    if client:
        client.close()

def get_database():
    return _database
