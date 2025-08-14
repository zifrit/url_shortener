import json

from schemas import ShortUrlCreate, FilmsCreate
from pydantic import HttpUrl
from api.v1.url_shortener.crud import storage, ShortUrlStorage
from api.v1.films.crud import fim_storage, FilmStorage


def load_data_from_json_file(
    json_file: str,
    model: ShortUrlCreate | FilmsCreate,
    storages: FilmStorage | ShortUrlStorage,
) -> None:
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not data:
                set_default_data()
            else:
                for item in data:
                    storages.create(model.model_validate(json.loads(item)))
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        set_default_data()


def dump_data_from_json_file(
    json_file: str,
    storages: FilmStorage | ShortUrlStorage,
) -> None:
    with open(json_file, "w", encoding="utf-8") as file:
        data = [value.model_dump_json() for key, value in storages.slug_to_item.items()]
        json.dump(data, file, indent=4, ensure_ascii=False)


def set_default_data() -> None:
    storage.create(
        ShortUrlCreate(
            taget_url=HttpUrl("https://www.google.com"),
            slug="google",
        ),
    )
    storage.create(
        ShortUrlCreate(
            taget_url=HttpUrl("https://www.example.com"),
            slug="search",
        ),
    )
    fim_storage.create(
        FilmsCreate(
            slug="avatar",
            name="Avatar",
            description="First amazing film",
            author="James Francis Cameron",
        ),
    )
    fim_storage.create(
        FilmsCreate(
            slug="avatar_2",
            name="Avatar2",
            description="Second amazing film",
            author="James Francis Cameron",
        ),
    )
    fim_storage.create(
        FilmsCreate(
            slug="avatar_3",
            name="Avatar3",
            description="Third amazing film",
            author="James Francis Cameron",
        ),
    )
