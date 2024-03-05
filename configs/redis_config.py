"""Configuration module for Redis"""
from huey import RedisHuey
from dotenv import load_dotenv

load_dotenv()

REDIS_APP_NAME = 'kv-store'
REDIS_HOST = 'redis'
REDIS_PORT = 6379

huey = RedisHuey(
    REDIS_APP_NAME,
    host=REDIS_HOST,
    port=REDIS_PORT,
)
