from typing import Dict, Type
from app.trainers.base_trainer import BaseTrainer

class TrainerRegistry:
    """Central registry mapping task types to concrete BaseTrainer implementations."""
    _registry: Dict[str, Type[BaseTrainer]] = {}

    @classmethod
    def register(cls, task_name: str, trainer_class: Type[BaseTrainer]):
        cls._registry[task_name.upper()] = trainer_class

    @classmethod
    def get(cls, task_name: str) -> Type[BaseTrainer]:
        key = task_name.upper()
        if key not in cls._registry:
            raise KeyError(
                f"No trainer registered for task '{task_name}'. "
                f"Available registered tasks: {list(cls._registry.keys())}"
            )
        return cls._registry[key]

    @classmethod
    def list_tasks(cls) -> list:
        return list(cls._registry.keys())

# Register default trainers
from app.trainers.tabular.tabular_trainer import TabularTrainer
from app.trainers.image.image_trainer import ImageTrainer
from app.trainers.text.text_trainer import TextTrainer
from app.trainers.timeseries.timeseries_trainer import TimeSeriesTrainer

TrainerRegistry.register("TABULAR_CLASSIFICATION", TabularTrainer)
TrainerRegistry.register("TABULAR_REGRESSION", TabularTrainer)
TrainerRegistry.register("IMAGE_CLASSIFICATION", ImageTrainer)
TrainerRegistry.register("TEXT_CLASSIFICATION", TextTrainer)
TrainerRegistry.register("TIME_SERIES_FORECASTING", TimeSeriesTrainer)
