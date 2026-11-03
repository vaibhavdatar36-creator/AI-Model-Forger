from typing import Any, Dict

class AIForgeModel:
    """Unified runtime model wrapper for loaded .aiforge packages."""

    def __init__(self, predictor, metadata: Dict[str, Any], schema: Dict[str, Any], manifest: Dict[str, Any]):
        self._predictor = predictor
        self.metadata = metadata
        self.schema = schema
        self.manifest = manifest

    @property
    def model_name(self) -> str:
        return self.metadata.get("model_name", "unnamed_model")

    @property
    def task(self) -> str:
        return self.metadata.get("task", "UNKNOWN")

    @property
    def modality(self) -> str:
        return self.metadata.get("modality", "UNKNOWN")

    @property
    def model_type(self) -> str:
        return self.metadata.get("model_type", "UNKNOWN")

    def predict(self, input_data: Any) -> Dict[str, Any]:
        """
        Unified prediction entry point:
        - Tabular: dict, list of dicts, or pandas DataFrame
        - Image: file path, bytes, or PIL Image
        - Text: string or list of strings
        - TimeSeries: dict or DataFrame
        """
        return self._predictor.predict(input_data)

    def summary(self) -> str:
        return (
            f"AIForgeModel(\n"
            f"  name='{self.model_name}',\n"
            f"  task='{self.task}',\n"
            f"  modality='{self.modality}',\n"
            f"  model_type='{self.model_type}',\n"
            f"  best_metric={self.metadata.get('best_metric_name')}={self.metadata.get('best_metric_value')}\n"
            f")"
        )

    def __repr__(self) -> str:
        return self.summary()
