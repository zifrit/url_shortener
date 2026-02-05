from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core import config
from storage import FilmStorage, ShortUrlStorage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.short_url_storage = ShortUrlStorage(
        hash_name=config.settings.redis.token.short_url,
    )
    app.state.film_storage = FilmStorage(hash_name=config.settings.redis.token.film)
    yield
