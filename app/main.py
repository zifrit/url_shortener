import logging

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from lifespan import lifespan
from web import router as web_router

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.include_router(web_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8000,
        reload=True,
        log_level=logging.DEBUG,
    )
