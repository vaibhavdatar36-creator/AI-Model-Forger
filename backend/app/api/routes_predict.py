import time
import base64
import sys
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db
from app.database.models import ModelArtifact
from app.schemas.requests import PredictRequest
from app.schemas.responses import PredictionResponse

# Ensure runtime_sdk is in sys.path
sdk_path = str(Path(__file__).resolve().parents[3] / "runtime_sdk")
if sdk_path not in sys.path:
    sys.path.insert(0, sdk_path)

from aiforge_runtime.loader import load_model

router = APIRouter(prefix="/api", tags=["predict"])

@router.post("/models/{model_id}/predict", response_model=PredictionResponse)
async def predict_with_model(
    model_id: str,
    request: PredictRequest,
    db: Session = Depends(get_db)
):
    art = db.query(ModelArtifact).filter(ModelArtifact.id == model_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Model artifact not found.")

    model_path = Path(art.file_path)
    if not model_path.exists():
        raise HTTPException(status_code=404, detail="Model artifact file missing on disk.")

    start_time = time.time()
    try:
        model = load_model(model_path)
        input_data = request.input_data

        # Check if input is base64 image
        if isinstance(input_data, str) and input_data.startswith("data:image"):
            # strip data url header
            base64_data = input_data.split(",")[1]
            input_data = base64.b64decode(base64_data)

        output = model.predict(input_data)
        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return PredictionResponse(
            success=True,
            prediction=output.get("prediction"),
            confidence=output.get("confidence"),
            probabilities=output.get("probabilities"),
            inference_time_ms=elapsed_ms
        )
    except Exception as e:
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return PredictionResponse(
            success=False,
            prediction=None,
            confidence=None,
            probabilities=None,
            inference_time_ms=elapsed_ms,
            error=str(e)
        )

@router.post("/models/{model_id}/predict_file")
async def predict_with_file(
    model_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Predict directly with uploaded image or file."""
    art = db.query(ModelArtifact).filter(ModelArtifact.id == model_id).first()
    if not art:
        raise HTTPException(status_code=404, detail="Model artifact not found.")

    model_path = Path(art.file_path)
    start_time = time.time()
    try:
        content = await file.read()
        model = load_model(model_path)
        output = model.predict(content)
        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "prediction": output.get("prediction"),
            "confidence": output.get("confidence"),
            "probabilities": output.get("probabilities"),
            "inference_time_ms": elapsed_ms
        }
    except Exception as e:
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "success": False,
            "prediction": None,
            "error": str(e),
            "inference_time_ms": elapsed_ms
        }
