from typing import Dict, Any, List, Optional
import pandas as pd

class SchemaDetector:
    """Generates standardized input schemas for model packages to validate future inference data."""

    @staticmethod
    def detect_tabular_schema(
        df: pd.DataFrame,
        feature_cols: List[str],
        target_col: Optional[str] = None
    ) -> Dict[str, Any]:
        features = {}
        for col in feature_cols:
            series = df[col]
            if pd.api.types.is_integer_dtype(series):
                col_type = "integer"
            elif pd.api.types.is_float_dtype(series):
                col_type = "float"
            elif pd.api.types.is_bool_dtype(series):
                col_type = "boolean"
            else:
                col_type = "string"

            # Top categories if string / categorical
            categories = None
            if col_type == "string" and series.nunique() <= 30:
                categories = [str(x) for x in series.dropna().unique().tolist()[:30]]

            features[col] = {
                "name": col,
                "type": col_type,
                "required": True,
                "categories": categories,
                "sample_values": [str(x) for x in series.dropna().head(3).tolist()]
            }

        target_info = None
        if target_col and target_col in df.columns:
            target_series = df[target_col]
            target_info = {
                "name": target_col,
                "type": "float" if pd.api.types.is_float_dtype(target_series) else "string",
                "classes": [str(x) for x in target_series.dropna().unique().tolist()] if not pd.api.types.is_float_dtype(target_series) else None
            }

        return {
            "format": "tabular",
            "features": features,
            "feature_names": feature_cols,
            "target": target_info
        }

    @staticmethod
    def detect_image_schema(image_size: tuple = (224, 224), channels: int = 3, classes: List[str] = None) -> Dict[str, Any]:
        return {
            "format": "image",
            "expected_shape": [channels, image_size[0], image_size[1]],
            "allowed_formats": [".jpg", ".jpeg", ".png", ".bmp", ".webp"],
            "channels": channels,
            "target": {
                "classes": classes or []
            }
        }

    @staticmethod
    def detect_text_schema(classes: List[str] = None) -> Dict[str, Any]:
        return {
            "format": "text",
            "expected_type": "string",
            "target": {
                "classes": classes or []
            }
        }
