from fastapi import HTTPException, BackgroundTasks
from starlette import status

from api.v1.films.crud import film_storage
from schemas import Films


def prefetch_film(
    slug: str,
) -> Films:

    if film := film_storage.get_by_slug(slug=slug):
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug} not found.",
    )


def save_film_state(
    background_task: BackgroundTasks,
):
    yield
    background_task.add_task(film_storage.save)
