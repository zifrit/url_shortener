import random
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status, Form

from api.v1.films.crud import FILMS
from schemas import Films
from services.dependencies.films import prefetch_film

router = APIRouter(prefix="/films")


@router.get("/", response_model=list[Films])
def read_film_list() -> list[Films]:
    return FILMS


@router.get("/{film_id}/", response_model=Films)
def read_film_list(film: Annotated[Films, Depends(prefetch_film)]) -> Films:
    return film


@router.post("/", response_model=Films, status_code=status.HTTP_201_CREATED)
def create_film(
    name: Annotated[
        str,
        Form(),
    ],
    description: Annotated[
        str,
        Form(),
    ],
    author: Annotated[
        str,
        Form(),
    ],
):
    return Films(
        film_id=random.randint(1, 100),
        name=name,
        description=description,
        author=author,
    )
