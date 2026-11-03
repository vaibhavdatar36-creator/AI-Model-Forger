import os
from pathlib import Path
from typing import Optional

TABULAR_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".json"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
TEXT_EXTENSIONS = {".txt", ".jsonl"}

def resolve_dataset_path(path: Path, modality: Optional[str] = None) -> Path:
    """
    Intelligently resolves the true dataset path from a file or directory.
    - If path is already a file, returns path.
    - If path is a directory:
        * If modality is IMAGE, returns the directory (for ImageTrainer).
        * If modality is TABULAR or TIME_SERIES, searches for the primary tabular file inside.
        * If modality is not specified, auto-inspects:
            - If it contains images and no tabular files, returns directory.
            - If it contains tabular files (e.g. CSV extracted from ZIP), returns the tabular file.
            - If it contains text files with subdirectories, returns directory.
    """
    path = Path(path)
    if not path.exists():
        return path

    if path.is_file():
        return path

    if path.is_dir():
        # If modality is explicitly IMAGE, computer vision expects the directory
        if modality == "IMAGE":
            return path

        img_files = [f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS]
        tab_files = [f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in TABULAR_EXTENSIONS]

        # Pure image directory
        if img_files and not tab_files:
            return path

        # Tabular dataset inside extracted directory
        if tab_files:
            if modality in ["TABULAR", "TIME_SERIES"] or not img_files:
                return tab_files[0]

        # Text files with class folders
        txt_files = [f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in TEXT_EXTENSIONS]
        if txt_files:
            subdirs = [d for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]
            if subdirs:
                return path
            return txt_files[0]

    return path
