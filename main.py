"""Configuration module for main app"""

from fastapi import FastAPI
from routers.data_router import router as datarouter

app = FastAPI()


app.include_router(datarouter)
