from fastapi import HTTPException
from starlette import status

from api.v1.films.crud import FILMS
from schemas import Films


def prefetch_film(
    film_id: int,
) -> Films:

    film = [film for film in FILMS if film.film_id == film_id]
    if film:
        return film[0]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {film_id} not found.",
    )
