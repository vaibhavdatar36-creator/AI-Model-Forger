import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import sanitize_filename, safe_extract_zip
from app.core.path_resolver import resolve_dataset_path
from app.core.logging import logger
from app.database.database import get_db
from app.database.models import Dataset
from app.services.modality_detector import ModalityDetector
from app.schemas.responses import UploadResponse

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload raw dataset file or ZIP archive.
    Performs security validation, extraction, modality identification, and registers dataset.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    clean_name = sanitize_filename(file.filename)
    ext = Path(clean_name).suffix.lower()

    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed formats: {sorted(list(settings.ALLOWED_EXTENSIONS))}"
        )

    dataset_id = str(uuid.uuid4())
    upload_dest_dir = settings.UPLOADS_DIR / dataset_id
    upload_dest_dir.mkdir(parents=True, exist_ok=True)
    saved_file_path = upload_dest_dir / clean_name

    # Stream file to disk while checking max size
    total_bytes = 0
    try:
        with open(saved_file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024): # 1MB chunks
                total_bytes += len(chunk)
                if total_bytes > settings.MAX_UPLOAD_SIZE_BYTES:
                    raise HTTPException(status_code=413, detail="Uploaded file exceeds 500MB maximum limit.")
                buffer.write(chunk)
    except Exception as e:
        if saved_file_path.exists():
            saved_file_path.unlink()
        raise e

    # If it is a zip file, safely extract it
    target_inspect_path = saved_file_path
    if ext == ".zip":
        extracted_dir = upload_dest_dir / f"extracted_{Path(clean_name).stem}"
        safe_extract_zip(saved_file_path, extracted_dir)
        target_inspect_path = extracted_dir
        # If archive contains a tabular file (e.g. CSV in zip), resolve directly to it
        resolved_file = resolve_dataset_path(extracted_dir)
        if resolved_file.is_file():
            target_inspect_path = resolved_file

    # Detect modality
    detection = ModalityDetector.detect(target_inspect_path)

    # Save to database
    db_dataset = Dataset(
        id=dataset_id,
        filename=clean_name,
        filepath=str(target_inspect_path),
        file_size=total_bytes,
        modality=detection["modality"],
        profile_json=detection
    )
    db.add(db_dataset)
    db.commit()

    return UploadResponse(
        dataset_id=dataset_id,
        filename=clean_name,
        file_size=total_bytes,
        modality=detection["modality"],
        confidence=detection["confidence"],
        message=f"Dataset successfully uploaded and analyzed as {detection['modality']}."
    )
