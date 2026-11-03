import re
from typing import Dict, Any, List, Optional
from app.core.logging import logger

class RuleBasedRequirementProvider:
    """Deterministic, robust natural language requirement extractor without external API dependency."""

    @staticmethod
    def analyze(requirement_text: str) -> Dict[str, Any]:
        text = requirement_text.lower().strip()
        
        # 1. Modality detection from prompt
        modality = "AUTO"
        modality_confidence = 0.8
        if any(w in text for w in ["image", "picture", "photo", "chest x-ray", "xray", "x-ray", "face", "vision", "camera", "mri"]):
            modality = "IMAGE"
            modality_confidence = 0.95
        elif any(w in text for w in ["review", "sentiment", "tweet", "message", "email", "spam", "text", "nlp", "sentence", "comment", "document", "article"]):
            modality = "TEXT"
            modality_confidence = 0.92
        elif any(w in text for w in ["tomorrow", "future", "forecast", "historical readings", "time series", "stock", "demand over time", "electricity demand", "hourly", "daily", "trend"]):
            modality = "TIME_SERIES"
            modality_confidence = 0.90
        elif any(w in text for w in ["sound", "audio", "voice", "speech", "bark", "siren", "noise", "acoustic"]):
            modality = "AUDIO"
            modality_confidence = 0.95
        elif any(w in text for w in ["video", "clip", "surveillance", "footage", "frames"]):
            modality = "VIDEO"
            modality_confidence = 0.95
        elif any(w in text for w in ["tabular", "csv", "table", "columns", "features", "churn", "price", "house", "salary", "loan", "customer"]):
            modality = "TABULAR"
            modality_confidence = 0.88

        # 2. Unsupported tasks check (Object Detection, Segmentation, OCR, Speech, Video)
        unsupported_task = None
        unsupported_message = None
        if any(w in text for w in ["detect object", "object detection", "detect cars", "detect pedestrians", "bounding box", "yolo", "locate objects"]):
            unsupported_task = "OBJECT_DETECTION"
            unsupported_message = "Your requirement appears to require Object Detection (bounding boxes). In Version 1, only Image Classification is active; Object Detection plugin is architected for a future update."
        elif any(w in text for w in ["segment", "segmentation", "mask", "pixel-level"]):
            unsupported_task = "IMAGE_SEGMENTATION"
            unsupported_message = "Image Segmentation is not currently active in Version 1."
        elif any(w in text for w in ["speech to text", "speech recognition", "transcribe", "transcription"]):
            unsupported_task = "SPEECH_RECOGNITION"
            unsupported_message = "Speech Recognition is scheduled for future audio plugin versions."
        elif any(w in text for w in ["recognize activities in video", "video classification", "action recognition"]):
            unsupported_task = "VIDEO_CLASSIFICATION"
            unsupported_message = "Video classification is computationally intensive and architected for a future release."

        # 3. Task type detection
        task = "UNKNOWN"
        task_confidence = 0.85
        if unsupported_task:
            task = unsupported_task
        elif any(w in text for w in ["predict", "forecast", "demand", "price", "cost", "value", "continuous", "temperature", "revenue", "sales"]):
            if modality == "TIME_SERIES":
                task = "TIME_SERIES_FORECASTING"
                task_confidence = 0.92
            elif modality == "TABULAR" or modality == "AUTO":
                task = "TABULAR_REGRESSION"
                task_confidence = 0.90
        
        if any(w in text for w in ["classify", "identify whether", "sentiment", "positive or negative", "spam or ham", "churn or not", "diagnose", "cats and dogs", "pneumonia or normal", "detect whether", "category", "label", "fraud", "churn"]):
            if modality == "IMAGE":
                task = "IMAGE_CLASSIFICATION"
                task_confidence = 0.96
            elif modality == "TEXT":
                task = "TEXT_CLASSIFICATION"
                task_confidence = 0.94
            elif modality == "TABULAR" or modality == "AUTO":
                task = "TABULAR_CLASSIFICATION"
                task_confidence = 0.92

        # 4. Target extraction heuristic
        target_candidate = None
        patterns = [
            r"predict (?:the )?([a-zA-Z0-9_\s]+?)(?: from| using| based on|\.|$)",
            r"classify (?:the )?([a-zA-Z0-9_\s]+?)(?: as| into| from|\.|$)",
            r"identify whether (?:a person has |an email is )?([a-zA-Z0-9_\s]+?)(?: from| based on|\.|$)",
            r"determine if (?:an? )?([a-zA-Z0-9_\s]+?)(?: is|\.|$)",
            r"target is ([a-zA-Z0-9_]+)",
            r"column ([a-zA-Z0-9_]+)"
        ]
        for pat in patterns:
            match = re.search(pat, text)
            if match:
                candidate = match.group(1).strip()
                if candidate and len(candidate) < 30 and candidate not in ["images", "data", "it", "this"]:
                    target_candidate = candidate
                    break

        return {
            "objective": requirement_text,
            "modality": modality,
            "modality_confidence": modality_confidence,
            "task": task,
            "task_confidence": task_confidence,
            "target_candidate": target_candidate,
            "unsupported_task": unsupported_task,
            "unsupported_message": unsupported_message,
            "is_supported": unsupported_task is None and task not in ["UNKNOWN", "AUDIO_CLASSIFICATION", "VIDEO_CLASSIFICATION"]
        }

class RequirementAnalyzer:
    """Main analyzer interface with extensible provider pattern."""
    
    def __init__(self, provider=None):
        self.provider = provider or RuleBasedRequirementProvider()

    def analyze(self, requirement: str) -> Dict[str, Any]:
        if not requirement or not requirement.strip():
            return {
                "objective": "",
                "modality": "AUTO",
                "modality_confidence": 0.5,
                "task": "UNKNOWN",
                "task_confidence": 0.5,
                "target_candidate": None,
                "unsupported_task": None,
                "unsupported_message": None,
                "is_supported": True
            }
        return self.provider.analyze(requirement)
