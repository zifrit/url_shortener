import logging

import uvicorn
from fastapi import FastAPI, Request

from api import router as api_router
from core.config import LOG_FORMAT, LOG_LEVEL
from lifespan import lifespan

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/",
        query="",
    )
    return {
        "message": f"Hello {name}",
        "docs_url": str(docs_url),
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8000,
        reload=True,
        log_level=logging.DEBUG,
    )
