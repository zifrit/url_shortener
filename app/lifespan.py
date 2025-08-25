from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.films.crud import film_storage
from app.api.v1.url_shortener.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
