from fastapi import FastAPI, BackgroundTasks
from api.api_v1.api import router as api_router

app = FastAPI()

@app.get("/")
async def root():
    return{'ARQ-API':'V1'}

app.include_router(api_router, prefix="/api/v1")