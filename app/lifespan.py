from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.films.crud import film_storage
from api.v1.url_shortener.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
