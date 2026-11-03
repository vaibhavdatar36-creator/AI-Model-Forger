from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    file_size: int
    modality: str
    confidence: float
    message: str

class ModelCandidateRecommendation(BaseModel):
    model_name: str
    display_name: str
    is_recommended: bool
    suitability_score: float # 0 to 1
    reasons: List[str]
    tradeoffs: List[str]

class AnalysisResponse(BaseModel):
    dataset_id: str
    requirement: str
    detected_modality: str
    modality_confidence: float
    modality_reasons: List[str]
    
    detected_task: str
    task_confidence: float
    is_supported: bool
    unsupported_message: Optional[str] = None
    
    suggested_target: Optional[str] = None
    target_confidence: float
    candidate_targets: List[str] = []
    
    data_summary: Dict[str, Any]
    quality_report: Dict[str, Any]
    
    recommended_models: List[ModelCandidateRecommendation]
    needs_user_confirmation: bool
    confirmation_prompt: Optional[str] = None

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    current_step: str
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    has_artifact: bool = False
    model_id: Optional[str] = None

class ModelArtifactSummary(BaseModel):
    id: str
    job_id: str
    name: str
    task: str
    modality: str
    model_type: str
    best_metric_name: str
    best_metric_value: float
    file_size: int
    created_at: datetime
    download_url: str

class JobResultResponse(BaseModel):
    job_id: str
    status: str
    dataset_summary: Dict[str, Any]
    data_processing_summary: List[str]
    model_comparisons: List[Dict[str, Any]]
    best_model_name: str
    best_metric_name: str
    best_metric_value: float
    model_artifact: Optional[ModelArtifactSummary] = None
    model_card: Dict[str, Any]
    confusion_matrix: Optional[Dict[str, Any]] = None
    training_time_seconds: float
    logs: str

class PredictionResponse(BaseModel):
    success: bool
    prediction: Any
    confidence: Optional[float] = None
    probabilities: Optional[Dict[str, float]] = None
    inference_time_ms: float
    error: Optional[str] = None
