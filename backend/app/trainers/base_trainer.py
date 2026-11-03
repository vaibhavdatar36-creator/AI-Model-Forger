from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable, Tuple
from pathlib import Path

class BaseTrainer(ABC):
    """Universal interface for all modality/task trainers."""

    def __init__(self, job_id: str, dataset_path: Path, requirement: str, options: Optional[Dict[str, Any]] = None):
        self.job_id = job_id
        self.dataset_path = Path(dataset_path)
        self.requirement = requirement
        self.options = options or {}
        self.trained_models = {}
        self.evaluations = {}
        self.best_model_name = None
        self.best_model_obj = None
        self.preprocessor = None
        self.schema = None
        self.metadata = {}
        self.data_processing_summary = []

    @abstractmethod
    def analyze_dataset(self) -> Dict[str, Any]:
        """Inspects and profiles the specific dataset structure."""
        pass

    @abstractmethod
    def prepare_data(self) -> Dict[str, Any]:
        """Preprocesses raw data into train/val/test splits."""
        pass

    @abstractmethod
    def recommend_models(self) -> List[Dict[str, Any]]:
        """Recommends candidate model architectures."""
        pass

    @abstractmethod
    def train(self, progress_callback: Optional[Callable[[int, str, Optional[Dict[str, Any]]], None]] = None) -> Dict[str, Any]:
        """Trains candidate models, notifying progress."""
        pass

    @abstractmethod
    def evaluate(self) -> Dict[str, Any]:
        """Evaluates all candidate models using appropriate metrics."""
        pass

    @abstractmethod
    def select_best_model(self) -> Tuple[str, Any, Dict[str, Any]]:
        """Selects the best performing model based on task-appropriate metric."""
        pass

    @abstractmethod
    def package_model(self, output_dir: Path) -> Path:
        """Packages best model and preprocessing pipeline into a single .aiforge file."""
        pass
