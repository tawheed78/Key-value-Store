"""Configuration module for Database"""
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = "mongodb+srv://tawheedchilwan55:TiGelbhH31VpQtM0@keyvalue.ygllhpj.mongodb.net/?retryWrites=true&w=majority&appName=keyvalue"

client = AsyncIOMotorClient(CONNECTION_STRING)

db = client["kv_store"]

try:
    client.admin.command("ping")
    print('ping')
except Exception as e:
    print(e)
