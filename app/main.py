from fastapi import FastAPI, Request
from api import router as api_router

app = FastAPI()
app.include_router(api_router)


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
