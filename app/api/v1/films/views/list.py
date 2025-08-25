from app.api.v1.films.crud import AlreadyExistFilmError, film_storage
from app.schemas import Films, FilmsCreate, FilmsRead
from fastapi import APIRouter, HTTPException, status

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
) -> Films | AlreadyExistFilmError:
    try:
        return film_storage.create_or_raise_if_exists(film)
    except AlreadyExistFilmError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Film with this slug={film.slug!r} already exists",
        )
