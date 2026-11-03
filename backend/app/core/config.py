import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(r"C:\Users\Vaibhav\.gemini\antigravity\scratch\ai-model-forge")
STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
MODELS_DIR = STORAGE_DIR / "models"
JOBS_DIR = STORAGE_DIR / "jobs"
DATABASE_URL = f"sqlite:///{STORAGE_DIR / 'aiforge.db'}"

# Ensure directories exist
for d in [STORAGE_DIR, UPLOADS_DIR, MODELS_DIR, JOBS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

class Settings(BaseModel):
    APP_NAME: str = "AI Model Forge"
    APP_VERSION: str = "1.0.0"
    TAGLINE: str = "Upload your data. Describe what you want. Get a ready-to-use AI model."
    BASE_DIR: Path = BASE_DIR
    STORAGE_DIR: Path = STORAGE_DIR
    UPLOADS_DIR: Path = UPLOADS_DIR
    MODELS_DIR: Path = MODELS_DIR
    JOBS_DIR: Path = JOBS_DIR
    DATABASE_URL: str = DATABASE_URL
    AIFORGE_FORMAT_VERSION: str = "1.0"
    
    # Upload limits
    MAX_UPLOAD_SIZE_BYTES: int = 500 * 1024 * 1024  # 500 MB
    ALLOWED_EXTENSIONS: set = {
        # Tabular
        ".csv", ".tsv", ".xlsx", ".xls", ".json", ".parquet",
        # Images
        ".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff",
        # Text
        ".txt", ".jsonl",
        # Audio / Video / Docs (Detected / Analyzed)
        ".wav", ".mp3", ".flac", ".ogg",
        ".mp4", ".avi", ".mov", ".mkv", ".webm",
        ".pdf", ".docx",
        # Archives
        ".zip", ".tar", ".gz"
    }

settings = Settings()
