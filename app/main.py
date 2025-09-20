import logging

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from api.main_views import router as main_router
from core.config import LOG_FORMAT, LOG_LEVEL
from lifespan import lifespan

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8000,
        reload=True,
        log_level=logging.DEBUG,
    )
