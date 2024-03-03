from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
# CONNECTION_STRING = os.getenv('CONNECTION_STRING')

CONNECTION_STRING = "mongodb+srv://tawheedchilwan55:TiGelbhH31VpQtM0@keyvalue.ygllhpj.mongodb.net/?retryWrites=true&w=majority&appName=keyvalue"

client = AsyncIOMotorClient(CONNECTION_STRING)

db = client["kv_store"]

try:
    client.admin.command("ping")
except Exception as e:
    print(e)
