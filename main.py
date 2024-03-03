from fastapi import FastAPI, Request
from routers.data_router import router as datarouter

app = FastAPI()


app.include_router(datarouter)
