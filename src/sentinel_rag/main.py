from fastapi import FastAPI

from .api import get_indexer, get_qa, router
from .config import get_settings
from .dependencies import build_indexer, build_qa

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Evidence-grounded repository intelligence API.",
)


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/", tags=["operations"])
def root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "message": "SentinelRAG API is running.",
        "docs": "/docs",
    }


app.include_router(router)
app.dependency_overrides[get_indexer] = build_indexer
app.dependency_overrides[get_qa] = build_qa
