import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.database.models import ModelArtifact
from app.schemas.responses import ModelArtifactSummary

router = APIRouter(prefix="/api", tags=["models"])

@router.get("/models", response_model=List[ModelArtifactSummary])
async def list_models(db: Session = Depends(get_db)):
    """List all trained model artifacts for training history."""
    artifacts = db.query(ModelArtifact).order_by(ModelArtifact.created_at.desc()).all()
    results = []
    for art in artifacts:
        results.append(ModelArtifactSummary(
            id=art.id,
            job_id=art.job_id,
            name=art.name,
            task=art.task,
            modality=art.modality,
            model_type=art.model_type,
            best_metric_name=art.best_metric_name,
            best_metric_value=art.best_metric_value,
            file_size=art.file_size,
            created_at=art.created_at,
            download_url=f"/api/models/{art.id}/download"
        ))
    return results

@router.get("/models/{model_id}")
async def get_model_details(model_id: str, db: Session = Depends(get_db)):
    art = db.query(ModelArtifact).filter(ModelArtifact.id == model_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Model artifact not found.")

    return {
        "id": art.id,
        "job_id": art.job_id,
        "name": art.name,
        "task": art.task,
        "modality": art.modality,
        "model_type": art.model_type,
        "best_metric_name": art.best_metric_name,
        "best_metric_value": art.best_metric_value,
        "metrics": art.metrics_json,
        "file_size": art.file_size,
        "schema": art.schema_json,
        "metadata": art.metadata_json,
        "download_url": f"/api/models/{art.id}/download",
        "created_at": art.created_at
    }

@router.get("/models/{model_id}/download")
async def download_model(model_id: str, db: Session = Depends(get_db)):
    """Download exactly ONE self-contained .aiforge model artifact."""
    art = db.query(ModelArtifact).filter(ModelArtifact.id == model_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Model artifact not found.")

    model_path = Path(art.file_path)
    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Model file is missing on server storage.")

    download_name = f"{art.name}.aiforge"
    return FileResponse(
        path=str(model_path),
        filename=download_name,
        media_type="application/octet-stream"
    )
