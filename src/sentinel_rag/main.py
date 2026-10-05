from fastapi import FastAPI

from .config import get_settings

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
