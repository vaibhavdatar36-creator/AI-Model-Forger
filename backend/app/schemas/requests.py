from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    dataset_id: str
    requirement: str = Field(..., description="Natural language description of what you want to achieve")
    target_column: Optional[str] = None
    override_modality: Optional[str] = None
    override_task: Optional[str] = None

class AdvancedSettings(BaseModel):
    target_column: Optional[str] = None
    task: Optional[str] = None
    modality: Optional[str] = None
    model_choice: Optional[str] = None # "auto" or specific model name
    test_size: float = 0.2
    random_seed: int = 42
    epochs: Optional[int] = None
    batch_size: Optional[int] = None

class TrainRequest(BaseModel):
    dataset_id: str
    requirement: str
    project_name: Optional[str] = "AI Project"
    model_selection_mode: str = "auto" # "auto" or "manual"
    selected_model: Optional[str] = None
    advanced_settings: Optional[AdvancedSettings] = None

class PredictRequest(BaseModel):
    input_data: Any = Field(..., description="Raw tabular dictionary, list of dicts, text string, or base64/image reference")
