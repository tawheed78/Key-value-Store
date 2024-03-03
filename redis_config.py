from huey import RedisHuey
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

huey = RedisHuey(
    APP_NAME,  # Replace with your app name
    host=HOST,  # Redis server hostname
    port=PORT,  # Redis server port
    # blocking=True,  # Use blocking-pop when reading from the queue
)
