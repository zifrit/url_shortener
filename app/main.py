import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
from schemas import ShortUrlCreate, FilmsCreate
from api import router as api_router
from api.v1.url_shortener.crud import storage
from api.v1.films.crud import fim_storage
from services.utils.load_dopm_data import (
    load_data_from_json_file,
    dump_data_from_json_file,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_data_from_json_file("film_slugs.json", FilmsCreate, fim_storage)
        load_data_from_json_file("short_url_slugs.json", ShortUrlCreate, storage)
        yield
        dump_data_from_json_file("short_url_slugs.json", storage)
        dump_data_from_json_file("film_slugs.json", fim_storage)
    finally:
        pass


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
