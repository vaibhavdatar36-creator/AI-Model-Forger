from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Dataset
from app.core.path_resolver import resolve_dataset_path
from app.services.modality_detector import ModalityDetector
from app.services.requirement_analyzer import RequirementAnalyzer
from app.services.task_detector import TaskDetector
from app.services.dataset_profiler import DatasetProfiler
from app.services.model_recommender import ModelRecommender
from app.schemas.requests import AnalyzeRequest
from app.schemas.responses import AnalysisResponse, ModelCandidateRecommendation

router = APIRouter(prefix="/api", tags=["analyze"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_dataset_and_requirement(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    dataset = db.query(Dataset).filter(Dataset.id == request.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    dataset_path = Path(dataset.filepath)
    if not dataset_path.exists():
        raise HTTPException(status_code=404, detail="Dataset file missing on disk.")

    # Resolve if dataset path points to an extracted directory containing tabular data
    resolved_path = resolve_dataset_path(dataset_path, modality=request.override_modality)
    if resolved_path != dataset_path and resolved_path.is_file():
        dataset.filepath = str(resolved_path)
        db.commit()
        dataset_path = resolved_path

    # 1. Modality detection
    modality_res = ModalityDetector.detect(dataset_path)
    detected_modality = request.override_modality or modality_res["modality"]
    modality_confidence = modality_res["confidence"]

    # 2. Natural language requirement analysis
    req_analyzer = RequirementAnalyzer()
    req_res = req_analyzer.analyze(request.requirement)

    # 3. Dataset profiling
    profile = DatasetProfiler.profile(
        file_or_dir_path=dataset_path,
        modality=detected_modality,
        requirement_target=request.target_column or req_res.get("target_candidate")
    )

    # 4. Task detection
    task_res = TaskDetector.detect(
        modality=detected_modality,
        requirement_analysis=req_res,
        dataset_profile=profile,
        target_column=request.target_column
    )

    detected_task = request.override_task or task_res["task"]
    task_confidence = task_res["confidence"]
    is_supported = task_res["is_supported"]
    unsupported_message = task_res.get("reason") if not is_supported else None

    # Target suggestions
    suggested_target = request.target_column or profile.get("suggested_target")
    candidate_targets = profile.get("candidate_targets", [])
    target_confidence = 0.92 if suggested_target else 0.5

    # 5. Model Recommendations
    model_recs = []
    if is_supported:
        model_recs = ModelRecommender.recommend(
            modality=detected_modality,
            task=detected_task,
            dataset_size_rows=profile.get("row_count", 1000)
        )

    # 6. Confidence evaluation / user confirmation
    needs_confirmation = False
    confirmation_prompt = None

    if len(candidate_targets) > 1 and not request.target_column and detected_modality == "TABULAR":
        needs_confirmation = True
        confirmation_prompt = f"I identified multiple potential target columns: {', '.join(candidate_targets[:3])}. We recommend '{suggested_target}'. Please confirm or select your preferred target."

    return AnalysisResponse(
        dataset_id=dataset.id,
        requirement=request.requirement,
        detected_modality=detected_modality,
        modality_confidence=modality_confidence,
        modality_reasons=modality_res.get("reasons", []),
        detected_task=detected_task,
        task_confidence=task_confidence,
        is_supported=is_supported,
        unsupported_message=unsupported_message,
        suggested_target=suggested_target,
        target_confidence=target_confidence,
        candidate_targets=candidate_targets,
        data_summary={
            "row_count": profile.get("row_count"),
            "col_count": profile.get("col_count"),
            "total_images": profile.get("total_images"),
            "classes": profile.get("classes"),
            "data_preview": profile.get("data_preview", [])[:5]
        },
        quality_report=profile.get("quality_report", {}),
        recommended_models=model_recs,
        needs_user_confirmation=needs_confirmation,
        confirmation_prompt=confirmation_prompt
    )
