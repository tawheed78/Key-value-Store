from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_STRING= os.environ.get('CONNECTION_STRING')

# Create a new client and connect to the server
client = AsyncIOMotorClient(CONNECTION_STRING)

db = client['kv_store']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
except Exception as e:
    print(e)

