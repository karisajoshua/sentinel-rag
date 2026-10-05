from fastapi import FastAPI

from .api import router, unavailable_indexer, unavailable_qa\nfrom .config import get_settings\nfrom .dependencies import build_indexer, build_qa

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
app.dependency_overrides[unavailable_indexer] = build_indexer
app.dependency_overrides[unavailable_qa] = build_qa
