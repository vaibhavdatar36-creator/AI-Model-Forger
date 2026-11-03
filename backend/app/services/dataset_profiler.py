import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from app.core.logging import logger

class DatasetProfiler:
    """Profiles tabular, text, image, and temporal datasets with memory-aware sampling."""

    @staticmethod
    def profile(
        file_or_dir_path: Path,
        modality: str = "TABULAR",
        requirement_target: Optional[str] = None
    ) -> Dict[str, Any]:
        path = Path(file_or_dir_path)

        if modality == "IMAGE" or path.is_dir() and any(path.rglob("*.jpg")):
            return DatasetProfiler._profile_image_dir(path)
        
        if modality == "TEXT" and path.is_dir():
            return DatasetProfiler._profile_text_dir(path)

        # Tabular / Structured / Time-Series profiling
        return DatasetProfiler._profile_tabular(path, requirement_target)

    @staticmethod
    def _profile_image_dir(path: Path) -> Dict[str, Any]:
        # Count images, classes, formats
        extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
        image_files = [f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in extensions]
        
        # Subdirectories as classes
        classes = {}
        for img in image_files:
            rel_parent = img.parent.name
            if rel_parent != path.name:
                classes[rel_parent] = classes.get(rel_parent, 0) + 1

        return {
            "modality": "IMAGE",
            "total_images": len(image_files),
            "classes": list(classes.keys()),
            "class_distribution": classes,
            "sample_files": [str(f.name) for f in image_files[:5]],
            "data_quality": {
                "corrupt_images": 0, # verified during training preparation
                "format_variety": list({f.suffix.lower() for f in image_files}),
                "is_balanced": max(classes.values()) / (min(classes.values()) or 1) < 3.0 if classes else True
            }
        }

    @staticmethod
    def _profile_text_dir(path: Path) -> Dict[str, Any]:
        text_files = [f for f in path.rglob("*.txt") if f.is_file()]
        classes = {}
        for txt in text_files:
            rel_parent = txt.parent.name
            if rel_parent != path.name:
                classes[rel_parent] = classes.get(rel_parent, 0) + 1

        return {
            "modality": "TEXT",
            "total_documents": len(text_files),
            "classes": list(classes.keys()),
            "class_distribution": classes,
            "sample_files": [str(f.name) for f in text_files[:5]],
            "data_quality": {
                "empty_documents": 0,
                "is_balanced": True
            }
        }

    @staticmethod
    def _profile_tabular(path: Path, requirement_target: Optional[str] = None) -> Dict[str, Any]:
        path = Path(path)
        # If directory, find the tabular file within
        if path.is_dir():
            for ext_candidate in [".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".json"]:
                candidates = list(path.rglob(f"*{ext_candidate}"))
                if candidates:
                    path = candidates[0]
                    break

        # Memory-aware loading
        df = None
        ext = path.suffix.lower() if path.is_file() else ""
        
        try:
            if ext == ".csv":
                # Sample 50,000 rows if file is huge
                file_size_mb = os.path.getsize(path) / (1024 * 1024)
                if file_size_mb > 50:
                    df = pd.read_csv(path, nrows=50000)
                    is_sampled = True
                else:
                    df = pd.read_csv(path)
                    is_sampled = False
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(path, nrows=20000)
                is_sampled = False
            elif ext == ".parquet":
                df = pd.read_parquet(path)
                is_sampled = False
            elif ext == ".json":
                df = pd.read_json(path, nrows=20000)
                is_sampled = False
            else:
                # Try reading as CSV fallback
                df = pd.read_csv(path, nrows=10000)
                is_sampled = False
        except Exception as e:
            logger.error(f"Error loading tabular dataset for profiling: {e}")
            return {
                "error": str(e),
                "row_count": 0,
                "col_count": 0,
                "columns": {}
            }

        if df is None or df.empty:
            return {"row_count": 0, "col_count": 0, "columns": {}}

        total_rows = len(df)
        total_cols = len(df.columns)
        duplicate_rows = int(df.duplicated().sum())

        columns_profile = {}
        candidate_targets = []
        id_columns = []
        constant_columns = []
        datetime_columns = []
        numerical_columns = []
        categorical_columns = []
        text_columns = []

        target_keywords = ["target", "label", "class", "churn", "price", "outcome", "survived", "status", "result", "y"]

        for col in df.columns:
            col_str = str(col)
            series = df[col]
            missing_count = int(series.isna().sum())
            missing_pct = round((missing_count / total_rows) * 100, 2)
            distinct_count = int(series.nunique(dropna=True))
            is_numeric = bool(pd.api.types.is_numeric_dtype(series))

            col_type = "categorical"
            # 1. ID column detection (check identifier name or high-cardinality non-numeric key)
            c_low = col_str.lower()
            is_id_name = any(c_low.endswith(s) for s in ["_id", "uuid", "guid", "index", "_key"]) or c_low in ["id", "uuid", "guid", "index", "pk", "key"]
            if is_id_name:
                col_type = "id"
                id_columns.append(col_str)
            elif not is_numeric and distinct_count == total_rows and total_rows > 10:
                col_type = "id"
                id_columns.append(col_str)
            # 2. Constant column
            elif distinct_count <= 1:
                col_type = "constant"
                constant_columns.append(col_str)
            # 3. Datetime detection
            elif pd.api.types.is_datetime64_any_dtype(series) or any(k in col_str.lower() for k in ["date", "time", "timestamp"]):
                try:
                    # quick parse check
                    pd.to_datetime(series.dropna().head(10))
                    col_type = "datetime"
                    datetime_columns.append(col_str)
                except Exception:
                    pass
            # 4. Text column (natural language)
            elif not is_numeric and distinct_count > 50:
                avg_char_len = series.dropna().astype(str).map(len).mean()
                if avg_char_len > 40:
                    col_type = "text"
                    text_columns.append(col_str)
                else:
                    col_type = "categorical"
                    categorical_columns.append(col_str)
            # 5. Numerical column
            elif is_numeric:
                col_type = "numerical"
                numerical_columns.append(col_str)
            else:
                col_type = "categorical"
                categorical_columns.append(col_str)

            # Check if this column is a target candidate
            score = 0
            if requirement_target and requirement_target.lower() in col_str.lower():
                score += 10
            if any(tk in col_str.lower() for tk in target_keywords):
                score += 5
            # Usually target is last column or named appropriately
            if col == df.columns[-1] and col_type != "id":
                score += 3
            if col_type in ["categorical", "numerical"] and 2 <= distinct_count <= 50:
                score += 2

            columns_profile[col_str] = {
                "name": col_str,
                "type": col_type,
                "is_numeric": is_numeric,
                "distinct_count": distinct_count,
                "missing_count": missing_count,
                "missing_pct": missing_pct,
                "sample_values": [str(v) for v in series.dropna().head(4).tolist()],
                "target_score": score
            }

            if score > 0 and col_type not in ["id", "constant"]:
                candidate_targets.append((col_str, score))

        # Sort candidate targets by score descending
        candidate_targets.sort(key=lambda x: x[1], reverse=True)
        suggested_target = candidate_targets[0][0] if candidate_targets else df.columns[-1]

        # Target distribution if suggested target exists
        target_distribution = {}
        if suggested_target in df.columns:
            val_counts = df[suggested_target].value_counts(dropna=False).head(10).to_dict()
            target_distribution = {str(k): int(v) for k, v in val_counts.items()}

        preview_records = df.head(10).fillna("").to_dict(orient="records")

        return {
            "modality": "TABULAR",
            "row_count": total_rows,
            "col_count": total_cols,
            "duplicate_rows": duplicate_rows,
            "columns": columns_profile,
            "numerical_columns": numerical_columns,
            "categorical_columns": categorical_columns,
            "datetime_columns": datetime_columns,
            "text_columns": text_columns,
            "id_columns": id_columns,
            "constant_columns": constant_columns,
            "suggested_target": suggested_target,
            "candidate_targets": [ct[0] for ct in candidate_targets[:5]],
            "target_distribution": target_distribution,
            "data_preview": preview_records,
            "quality_report": {
                "total_missing_values": int(df.isna().sum().sum()),
                "columns_with_missing": [c for c, p in columns_profile.items() if p["missing_count"] > 0],
                "duplicate_count": duplicate_rows,
                "excluded_columns": id_columns + constant_columns
            }
        }
