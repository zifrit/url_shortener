import random
from typing import Annotated

from fastapi import APIRouter, Depends, status, Form

from api.v1.films.crud import fim_storage
from schemas import Films, FilmsCreate
from services.dependencies.films import prefetch_film

router = APIRouter(prefix="/films")


@router.get("/", response_model=list[Films])
def read_film_list() -> list[Films]:
    return fim_storage.get()


@router.get("/{slug}/", response_model=Films)
def read_film_list(film: Annotated[Films, Depends(prefetch_film)]) -> Films:
    return film


@router.post("/", response_model=Films, status_code=status.HTTP_201_CREATED)
def create_film(film: FilmsCreate):
    return fim_storage.create(film)
