from typing import Annotated

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from schemas.short_url import ShortUrl

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
