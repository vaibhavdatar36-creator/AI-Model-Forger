"""
AI Forge Runtime SDK
Universal inference runtime for single-file .aiforge model artifacts.
"""
from .loader import load_model
from .model import AIForgeModel

__version__ = "1.0.0"
__all__ = ["load_model", "AIForgeModel"]
