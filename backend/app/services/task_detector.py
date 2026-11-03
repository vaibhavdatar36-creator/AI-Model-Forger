from typing import Dict, Any, Optional
from app.core.logging import logger

SUPPORTED_TASKS = {
    "TABULAR_CLASSIFICATION",
    "TABULAR_REGRESSION",
    "IMAGE_CLASSIFICATION",
    "TEXT_CLASSIFICATION",
    "TIME_SERIES_FORECASTING"
}

class TaskDetector:
    """Harmonizes dataset modality, column metadata, and natural language requirements to determine task."""

    @staticmethod
    def detect(
        modality: str,
        requirement_analysis: Dict[str, Any],
        dataset_profile: Optional[Dict[str, Any]] = None,
        target_column: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Check if user requirement requested an unsupported task
        if requirement_analysis.get("unsupported_task"):
            return {
                "task": requirement_analysis["unsupported_task"],
                "confidence": 0.95,
                "is_supported": False,
                "reason": requirement_analysis.get("unsupported_message", "Task is not supported in Version 1.")
            }

        # 2. Match by modality
        req_task = requirement_analysis.get("task", "UNKNOWN")

        if modality == "IMAGE":
            return {
                "task": "IMAGE_CLASSIFICATION",
                "confidence": 0.96,
                "is_supported": True,
                "reason": "Image dataset detected. Standard task is Image Classification."
            }

        if modality == "TEXT":
            return {
                "task": "TEXT_CLASSIFICATION",
                "confidence": 0.94,
                "is_supported": True,
                "reason": "Text dataset detected. Standard task is Text Classification."
            }

        if modality == "TIME_SERIES":
            return {
                "task": "TIME_SERIES_FORECASTING",
                "confidence": 0.92,
                "is_supported": True,
                "reason": "Temporal structure with timestamp and numerical metric detected."
            }

        if modality == "AUDIO":
            return {
                "task": "AUDIO_CLASSIFICATION",
                "confidence": 0.90,
                "is_supported": False,
                "reason": "Audio dataset detected. Supported architecture, trainer plugin coming in future version."
            }

        if modality == "VIDEO":
            return {
                "task": "VIDEO_CLASSIFICATION",
                "confidence": 0.90,
                "is_supported": False,
                "reason": "Video dataset detected. Video classification is computationally heavy and marked for future releases."
            }

        if modality == "DOCUMENT":
            return {
                "task": "TEXT_CLASSIFICATION",
                "confidence": 0.88,
                "is_supported": True,
                "reason": "Document dataset detected. Processing text extraction into text classification pipeline."
            }

        # Tabular Task Detection (Classification vs Regression)
        # If target column is known/inferred, inspect target data
        if dataset_profile and "columns" in dataset_profile:
            target_info = None
            if target_column and target_column in dataset_profile["columns"]:
                target_info = dataset_profile["columns"][target_column]
            elif dataset_profile.get("suggested_target"):
                st = dataset_profile["suggested_target"]
                if st in dataset_profile["columns"]:
                    target_info = dataset_profile["columns"][st]

            if target_info:
                # If target is categorical or low distinct values (< 20) -> classification
                distinct_count = target_info.get("distinct_count", 0)
                is_numeric = target_info.get("is_numeric", False)
                
                if not is_numeric or distinct_count <= 10:
                    return {
                        "task": "TABULAR_CLASSIFICATION",
                        "confidence": 0.94,
                        "is_supported": True,
                        "reason": f"Target column '{target_info['name']}' has {distinct_count} distinct categories."
                    }
                else:
                    return {
                        "task": "TABULAR_REGRESSION",
                        "confidence": 0.92,
                        "is_supported": True,
                        "reason": f"Target column '{target_info['name']}' is a continuous numerical variable."
                    }

        # Fallback to requirement task if tabular profiling didn't conclude
        if req_task in ["TABULAR_REGRESSION", "TABULAR_CLASSIFICATION"]:
            return {
                "task": req_task,
                "confidence": requirement_analysis.get("task_confidence", 0.85),
                "is_supported": True,
                "reason": f"Inferred from natural language requirement: {req_task}"
            }

        # Default fallback for tabular
        return {
            "task": "TABULAR_CLASSIFICATION",
            "confidence": 0.80,
            "is_supported": True,
            "reason": "Defaulting to Tabular Classification for structured data."
        }
