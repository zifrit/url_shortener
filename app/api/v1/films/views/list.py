from fastapi import status

from api.v1.films.crud import fim_storage
from schemas import Films, FilmsCreate
from fastapi import APIRouter

router = APIRouter(prefix="/films")


@router.get("/", response_model=list[Films])
def read_film_list() -> list[Films]:
    return fim_storage.get()


@router.post("/", response_model=Films, status_code=status.HTTP_201_CREATED)
def create_film(film: FilmsCreate):
    return fim_storage.create(film)
