from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from schemas.short_url import ShortUrl

SHORT_URL = [
    ShortUrl(
        taget_url="http://www.example.com",
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
    slug: str,
):
    url: ShortUrl | None = next(
        (url for url in SHORT_URL if url.slug == slug),
        None,
    )
    if url:
        return RedirectResponse(url=url.taget_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'"{slug}" Not found.',
    )
