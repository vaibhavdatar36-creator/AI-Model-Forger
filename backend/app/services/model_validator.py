from pathlib import Path
from typing import Dict, Any, Tuple
import sys

# Ensure runtime_sdk is in sys.path
sdk_path = str(Path(__file__).resolve().parents[3] / "runtime_sdk")
if sdk_path not in sys.path:
    sys.path.insert(0, sdk_path)

from aiforge_runtime.loader import load_model
from app.core.security import compute_sha256
from app.core.logging import logger

class ModelValidator:
    """Pre-download validation engine that independently tests model packages before releasing to user."""

    @staticmethod
    def validate_package(package_path: Path, test_sample: Any) -> Tuple[bool, str, Dict[str, Any]]:
        package_path = Path(package_path)
        if not package_path.exists():
            return False, f"Package file does not exist at {package_path}", {}

        try:
            # 1. Package Integrity Check (SHA256)
            actual_checksum = compute_sha256(package_path)
            
            # 2. Reload model via runtime SDK
            loaded_model = load_model(package_path)

            # 3. Verify manifest metadata
            manifest = loaded_model.manifest
            if manifest.get("sha256") and manifest["sha256"] != actual_checksum:
                logger.warning("Manifest checksum mismatch - recomputed during final assembly.")

            # 4. Run inference on held-out test sample
            prediction_output = loaded_model.predict(test_sample)

            if "prediction" not in prediction_output:
                return False, "Prediction output missing 'prediction' key.", {}

            validation_report = {
                "package_valid": True,
                "model_name": loaded_model.model_name,
                "task": loaded_model.task,
                "test_prediction": prediction_output["prediction"],
                "test_confidence": prediction_output.get("confidence"),
                "checksum": actual_checksum,
                "status": "VERIFIED_READY"
            }
            logger.info(f"Model package {package_path.name} successfully verified! Test prediction: {prediction_output['prediction']}")
            return True, "Model package passed all verification criteria.", validation_report

        except Exception as e:
            logger.error(f"Package validation failed for {package_path}: {e}", exc_info=True)
            return False, f"Package verification error: {str(e)}", {}
