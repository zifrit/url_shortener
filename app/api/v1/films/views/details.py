from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from starlette import status

from api.v1.films.crud import film_storage
from schemas import Films, FilmsUpdate, FilmsParticularUpdate, FilmsRead
from services.dependencies.films import prefetch_film
from services.dependencies.other import api_token_validate

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
    dependencies=[
        Depends(api_token_validate),
    ],
)

FilmBySlug = Annotated[
    Films,
    Depends(prefetch_film),
]


@router.get("/", response_model=FilmsRead)
def read_film_by_slug(film: Annotated[Films, Depends(prefetch_film)]) -> Films:
    return film


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    film: FilmBySlug,
) -> None:
    film_storage.delete(film)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=FilmsRead,
)
def update_film_details(
    film: FilmBySlug,
    film_in: FilmsUpdate,
) -> Films:
    return film_storage.update(film=film, film_in=film_in)


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=FilmsRead,
)
def update_film_details(
    film: FilmBySlug,
    film_in: FilmsParticularUpdate,
) -> Films:
    return film_storage.particular_update(film=film, film_in=film_in)
