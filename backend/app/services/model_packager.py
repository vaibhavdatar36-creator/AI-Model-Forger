import os
import json
import hashlib
import tempfile
import zipfile
import platform
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import joblib
from app.core.config import settings
from app.core.security import compute_sha256
from app.core.logging import logger

class ModelPackager:
    """Packages model, preprocessing pipeline, schemas, and metadata into a single .aiforge file."""

    @staticmethod
    def package(
        output_filepath: Path,
        model_obj: Any,
        preprocessor_obj: Any,
        metadata: Dict[str, Any],
        schema: Dict[str, Any],
        predictor_type: str, # "tabular", "image", "text", "timeseries"
        extra_assets: Optional[Dict[str, bytes]] = None
    ) -> Path:
        output_filepath = Path(output_filepath)
        output_filepath.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            model_dir = temp_path / "model"
            prep_dir = temp_path / "preprocessing"
            model_dir.mkdir()
            prep_dir.mkdir()

            # 1. Save Preprocessing
            if preprocessor_obj is not None:
                joblib.dump(preprocessor_obj, prep_dir / "preprocessor.joblib", compress=3)

            # 2. Save Model Object (PyTorch or Scikit-learn/Joblib)
            if predictor_type == "image":
                import torch
                # If torch module, save state_dict or entire module
                torch.save(model_obj, model_dir / "model.pt")
            else:
                joblib.dump(model_obj, model_dir / "model.joblib", compress=3)

            # 3. Extra assets (e.g. label encoder, class maps, vocabulary)
            if extra_assets:
                for asset_name, asset_bytes in extra_assets.items():
                    asset_file = temp_path / asset_name
                    asset_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(asset_file, "wb") as f:
                        f.write(asset_bytes)

            # 4. Save metadata and schema
            with open(temp_path / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, default=str)

            with open(temp_path / "schema.json", "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2, default=str)

            # 5. Save runtime config
            runtime_config = {
                "format_version": settings.AIFORGE_FORMAT_VERSION,
                "predictor_type": predictor_type,
                "python_version": sys.version.split()[0],
                "platform": platform.platform(),
                "libraries": {
                    "scikit-learn": "1.4+",
                    "torch": "2.2+",
                    "pandas": "2.0+",
                    "numpy": "1.26+"
                }
            }
            with open(temp_path / "runtime_config.json", "w", encoding="utf-8") as f:
                json.dump(runtime_config, f, indent=2)

            # 6. Build Manifest and compute content hashes
            content_hasher = hashlib.sha256()
            files_list = []
            for p in sorted(temp_path.rglob("*")):
                if p.is_file():
                    rel_p = str(p.relative_to(temp_path)).replace("\\", "/")
                    files_list.append(rel_p)
                    content_hasher.update(rel_p.encode())
                    with open(p, "rb") as bf:
                        while ch := bf.read(65536):
                            content_hasher.update(ch)

            manifest = {
                "format": "AIFORGE",
                "format_version": settings.AIFORGE_FORMAT_VERSION,
                "model_name": metadata.get("model_name", "unnamed_model"),
                "task": metadata.get("task", "UNKNOWN"),
                "modality": metadata.get("modality", "UNKNOWN"),
                "created_at": metadata.get("created_at"),
                "sha256": content_hasher.hexdigest(),
                "files": files_list + ["manifest.json"]
            }
            with open(temp_path / "manifest.json", "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)

            # 7. Create single .aiforge zip archive cleanly
            temp_archive = temp_path.parent / f"{output_filepath.stem}.tmp.zip"
            with zipfile.ZipFile(temp_archive, "w", zipfile.ZIP_DEFLATED) as zf:
                for file_p in temp_path.rglob("*"):
                    if file_p.is_file():
                        arcname = file_p.relative_to(temp_path)
                        zf.write(file_p, arcname)

            if output_filepath.exists():
                output_filepath.unlink()
            os.rename(temp_archive, output_filepath)

        logger.info(f"Model successfully packaged into single artifact: {output_filepath} (Size: {os.path.getsize(output_filepath):,} bytes)")
        return output_filepath
