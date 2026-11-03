from abc import ABC, abstractmethod
from typing import Any, Dict

class BasePredictor(ABC):
    def __init__(self, model_obj: Any, preprocessor_obj: Any, schema: Dict[str, Any], metadata: Dict[str, Any]):
        self.model = model_obj
        self.preprocessor = preprocessor_obj
        self.schema = schema
        self.metadata = metadata

    @abstractmethod
    def predict(self, input_data: Any) -> Dict[str, Any]:
        """Perform preprocessing and inference on raw input data and return standardized result."""
        pass
