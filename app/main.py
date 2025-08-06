from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from schemas import ShortUrl, Films

SHORT_URL = [
    ShortUrl(
        taget_url="http://www.google.com",
        slug="google",
    ),
    ShortUrl(
        taget_url="http://www.example.com",
        slug="search",
    ),
]


FILMS = [
    Films(
        film_id=1,
        name="Avatar",
        description="First amazing film",
        author="James Francis Cameron",
    ),
    Films(
        film_id=2,
        name="Avatar2",
        description="Second amazing film",
        author="James Francis Cameron",
    ),
    Films(
        film_id=3,
        name="Avatar2",
        description="Third amazing film",
        author="James Francis Cameron",
    ),
]
app = FastAPI(
    title="Url Shortener",
)


def prefetch_slug_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = next(
        (url for url in SHORT_URL if url.slug == slug),
        None,
    )
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'"{slug}" Not found.',
    )


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


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/",
        query="",
    )
    return {
        "message": f"Hello {name}",
        "docs_url": str(docs_url),
    }


@app.get("/short-urls/", response_model=list[ShortUrl])
def read_short_url_list(request: Request) -> list[ShortUrl]:
    return SHORT_URL


@app.get("/r/{slug}/")
def redirect_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_slug_url),
    ],
):
    return RedirectResponse(url=url.taget_url)


@app.get(
    "/short-urls/{slug}/",
    response_model=ShortUrl,
)
def info_short_urls(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_slug_url),
    ],
):
    return url


@app.get("/films/", response_model=list[Films])
def read_film_list() -> list[Films]:
    return FILMS


@app.get("/films/{film_id}/", response_model=Films)
def read_film_list(film: Annotated[Films, Depends(prefetch_film)]) -> Films:
    return film
