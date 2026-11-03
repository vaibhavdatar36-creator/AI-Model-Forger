from typing import Dict, Any, List, Optional
import pandas as pd

class SchemaValidationError(Exception):
    pass

class SchemaValidator:
    """Validates runtime inputs against model package input schema."""

    @staticmethod
    def validate_tabular(input_data: Any, schema: Dict[str, Any]) -> pd.DataFrame:
        expected_features = schema.get("feature_names", [])

        # Convert dict or list of dicts to DataFrame
        if isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        elif isinstance(input_data, list):
            df = pd.DataFrame(input_data)
        elif isinstance(input_data, pd.DataFrame):
            df = input_data.copy()
        else:
            raise SchemaValidationError(f"Expected dict, list of dicts, or pandas DataFrame. Received {type(input_data).__name__}.")

        # Check for missing required features
        missing = [f for f in expected_features if f not in df.columns]
        if missing:
            raise SchemaValidationError(f"Missing required feature(s) for inference: {missing}. Expected features: {expected_features}")

        # Reorder columns to exact expected training order
        df = df[expected_features]
        return df

    @staticmethod
    def validate_text(input_data: Any) -> List[str]:
        if isinstance(input_data, str):
            return [input_data]
        elif isinstance(input_data, list) and all(isinstance(x, str) for x in input_data):
            return input_data
        else:
            raise SchemaValidationError(f"Expected text string or list of text strings. Received {type(input_data).__name__}.")
