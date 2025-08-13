from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.v1.films.crud import fim_storage
from schemas import Films, FilmsUpdate
from services.dependencies.films import prefetch_film

router = APIRouter(
    prefix="/{slug}",
    responses={
        # status.HTTP_204_NO_CONTENT: None,
        status.HTTP_404_NOT_FOUND: {
            "description": "Film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Film 'slug' not found",
                    },
                },
            },
        },
    },
)

FilmBySlug = Annotated[
    Films,
    Depends(prefetch_film),
]


@router.get("/", response_model=Films)
def read_film_by_slug(film: Annotated[Films, Depends(prefetch_film)]) -> Films:
    return film


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    film: FilmBySlug,
) -> None:
    fim_storage.delete(film)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Films,
)
def update_film_details(
    film: FilmBySlug,
    film_in: FilmsUpdate,
) -> Films:
    updated_film = fim_storage.update(film=film, film_in=film_in)
    return updated_film
