from fastapi import status, Depends

from api.v1.films.crud import film_storage
from schemas import Films, FilmsCreate, FilmsRead
from fastapi import APIRouter, BackgroundTasks

from services.dependencies.films import save_film_state

router = APIRouter(prefix="/films", dependencies=[Depends(save_film_state)])


@router.get("/", response_model=list[FilmsRead])
def read_film_list() -> list[Films]:
    return film_storage.get()


@router.post("/", response_model=FilmsRead, status_code=status.HTTP_201_CREATED)
def create_film(
    film: FilmsCreate,
):
    return film_storage.create(film)
