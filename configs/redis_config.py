"""Configuration module for Redis"""

import os
from huey import RedisHuey
from dotenv import load_dotenv

load_dotenv()

# REDIS_APP_NAME = os.getenv("REDIS_APP_NAME")
# REDIS_HOST = os.getenv("REDIS_HOST")
# REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_APP_NAME = 'kv-store'
REDIS_HOST = 'redis'
REDIS_PORT = 6379

huey = RedisHuey(
    REDIS_APP_NAME,  # Replace with your app name
    host=REDIS_HOST,  # Redis server hostname
    port=REDIS_PORT,  # Redis server port
    # blocking=True,  # Use blocking-pop when reading from the queue
)
