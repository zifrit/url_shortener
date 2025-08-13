from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.v1.films.crud import fim_storage
from schemas import Films
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


@router.get("/", response_model=Films)
def read_film_by_slug(film: Annotated[Films, Depends(prefetch_film)]) -> Films:
    return film


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
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
def delete_film(
    film: Annotated[
        Films,
        Depends(prefetch_film),
    ],
) -> None:
    fim_storage.delete(film)
