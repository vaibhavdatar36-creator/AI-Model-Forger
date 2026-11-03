import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Ensure backend root and runtime_sdk are in python path
backend_dir = Path(__file__).resolve().parent.parent
sdk_dir = Path(__file__).resolve().parents[2] / "runtime_sdk"
for p in [str(backend_dir), str(sdk_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.core.config import settings
from app.core.logging import logger
from app.database.database import engine, Base
from app.api import routes_upload, routes_analyze, routes_train, routes_models, routes_predict
from app.utils.hardware import get_hardware_info

# Initialize Database Schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Universal Multimodal AutoML Platform - Train, evaluate, package, and download ready-to-use AI models in single .aiforge files."
)

# CORS Middleware (allows frontend on Vite dev server port 5173 or other origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(routes_upload.router)
app.include_router(routes_analyze.router)
app.include_router(routes_train.router)
app.include_router(routes_models.router)
app.include_router(routes_predict.router)

@app.get("/api/health")
async def health_check():
    hw = get_hardware_info()
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "hardware": hw,
        "supported_modalities": ["TABULAR", "IMAGE", "TEXT", "TIME_SERIES"],
        "package_format": settings.AIFORGE_FORMAT_VERSION
    }

# Mount Frontend Static Assets if built
frontend_dist = settings.BASE_DIR / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
