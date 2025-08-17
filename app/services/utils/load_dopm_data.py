# from pathlib import Path
#
# from schemas import ShortUrlCreate, FilmsCreate
# from pydantic import HttpUrl, ValidationError
#
# from api.v1.films.crud import FilmStorage
#
# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from api.v1.url_shortener.crud import ShortUrlStorage
#
#
# # def load_film_data(
# #     json_file_url: Path,
# # ) -> FilmStorage:
# #     try:
# #         if not json_file_url.exists():
# #             storage = FilmStorage()
# #             set_default_film_data(storage)
# #             return storage
# #         return FilmStorage.model_validate_json(json_file_url.read_text())
# #     except ValidationError:
# #         storage = FilmStorage()
# #         set_default_film_data(storage)
# #         return storage
# #
# #
# # def load_short_url_data(
# #     json_file_url: Path,
# # ) -> ShortUrlStorage:
# #     try:
# #         if not json_file_url.exists():
# #             storage = ShortUrlStorage()
# #             set_default_url_short_data(storage)
# #             return storage
# #         return ShortUrlStorage.model_validate_json(json_file_url.read_text())
# #     except ValidationError:
# #         storage = ShortUrlStorage()
# #         set_default_url_short_data(storage)
# #         return storage
#
#
# def dump_data_from_json_file(
#     json_file_url: Path,
#     storages: FilmStorage | ShortUrlStorage,
# ) -> None:
#     json_file_url.write_text(storages.model_dump_json(indent=2))
#
#
# def set_default_url_short_data(storage: "ShortUrlStorage") -> "ShortUrlStorage":
#     storage.create(
#         ShortUrlCreate(
#             taget_url=HttpUrl("https://www.google.com"),
#             slug="google",
#         ),
#     )
#     storage.create(
#         ShortUrlCreate(
#             taget_url=HttpUrl("https://www.example.com"),
#             slug="search",
#         ),
#     )
#     return storage
#
#
# def set_default_film_data(storage: FilmStorage) -> None:
#     storage.create(
#         FilmsCreate(
#             slug="avatar",
#             name="Avatar",
#             description="First amazing film",
#             author="James Francis Cameron",
#         ),
#     )
#     storage.create(
#         FilmsCreate(
#             slug="avatar_2",
#             name="Avatar2",
#             description="Second amazing film",
#             author="James Francis Cameron",
#         ),
#     )
#     storage.create(
#         FilmsCreate(
#             slug="avatar_3",
#             name="Avatar3",
#             description="Third amazing film",
#             author="James Francis Cameron",
#         ),
#     )
