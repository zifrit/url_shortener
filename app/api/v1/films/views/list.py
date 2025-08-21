from fastapi import status, HTTPException

from api.v1.films.crud import film_storage
from schemas import Films, FilmsCreate, FilmsRead
from fastapi import APIRouter, BackgroundTasks


router = APIRouter(
    prefix="/films",
)


@router.get("/", response_model=list[FilmsRead])
def read_film_list() -> list[Films]:
    return film_storage.get()


@router.post(
    "/",
    response_model=FilmsRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Invalid request",
            "content": {
                "application/json": {
                    "example": {"detail": "Film with slug='foobar' already exists."},
                },
            },
        },
    },
)
def create_film(
    film: FilmsCreate,
):
    if not film_storage.get_by_slug(film.slug):
        return film_storage.create(film)
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Film with this slug={film.slug!r} already exists",
    )
