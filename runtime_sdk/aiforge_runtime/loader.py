import os
import json
import zipfile
import tempfile
from pathlib import Path
from typing import Union
import joblib

from .model import AIForgeModel
from .predictors.tabular import TabularPredictor
from .predictors.image import ImagePredictor
from .predictors.text import TextPredictor
from .predictors.timeseries import TimeSeriesPredictor

def load_model(package_path: Union[str, Path]) -> AIForgeModel:
    """
    Load a trained .aiforge model artifact into a ready-to-use AIForgeModel instance.
    Handles archive extraction, schema verification, preprocessor restoration, and model weights.
    """
    path = Path(package_path)
    if not path.exists():
        raise FileNotFoundError(f"Model package artifact not found at: {path}")

    with tempfile.TemporaryDirectory() as extract_dir:
        temp_dir = Path(extract_dir)

        # Extract archive safely
        with zipfile.ZipFile(path, 'r') as zf:
            for member in zf.infolist():
                # Security: prevent path traversal
                dest = (temp_dir / member.filename).resolve()
                if not dest.is_relative_to(temp_dir.resolve()):
                    raise SecurityError(f"Malicious file path detected in model package: {member.filename}")
                zf.extract(member, temp_dir)

        # Read manifest, metadata, schema, runtime_config
        manifest_path = temp_dir / "manifest.json"
        metadata_path = temp_dir / "metadata.json"
        schema_path = temp_dir / "schema.json"
        runtime_config_path = temp_dir / "runtime_config.json"

        if not manifest_path.exists() or not metadata_path.exists() or not schema_path.exists():
            raise ValueError(f"Corrupt or invalid .aiforge artifact: Missing essential descriptor files.")

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)

        runtime_config = {}
        if runtime_config_path.exists():
            with open(runtime_config_path, "r", encoding="utf-8") as f:
                runtime_config = json.load(f)

        predictor_type = runtime_config.get("predictor_type", metadata.get("modality", "tabular").lower())

        # Load Preprocessor
        preprocessor = None
        prep_file = temp_dir / "preprocessing" / "preprocessor.joblib"
        if prep_file.exists():
            preprocessor = joblib.load(prep_file)

        # Load Model
        model_obj = None
        if predictor_type == "image":
            import torch
            model_pt = temp_dir / "model" / "model.pt"
            if not model_pt.exists():
                raise FileNotFoundError("PyTorch model weights not found in package.")
            model_obj = torch.load(model_pt, map_location="cpu", weights_only=False)
            model_obj.eval()
            predictor = ImagePredictor(model_obj, preprocessor, schema, metadata)
        elif predictor_type == "text":
            model_joblib = temp_dir / "model" / "model.joblib"
            model_obj = joblib.load(model_joblib)
            predictor = TextPredictor(model_obj, preprocessor, schema, metadata)
        elif predictor_type in ["timeseries", "time_series"]:
            model_joblib = temp_dir / "model" / "model.joblib"
            model_obj = joblib.load(model_joblib)
            predictor = TimeSeriesPredictor(model_obj, preprocessor, schema, metadata)
        else: # tabular
            model_joblib = temp_dir / "model" / "model.joblib"
            model_obj = joblib.load(model_joblib)
            predictor = TabularPredictor(model_obj, preprocessor, schema, metadata)

        return AIForgeModel(
            predictor=predictor,
            metadata=metadata,
            schema=schema,
            manifest=manifest
        )
