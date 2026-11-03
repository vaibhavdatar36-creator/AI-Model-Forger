from typing import Any, Dict, List
import pandas as pd
import numpy as np
from .base import BasePredictor

class TimeSeriesPredictor(BasePredictor):
    def predict(self, input_data: Any) -> Dict[str, Any]:
        """
        Accepts:
            - DataFrame with features/lags
            - Dict with feature values
        """
        if isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        elif isinstance(input_data, pd.DataFrame):
            df = input_data.copy()
        else:
            raise TypeError("Expected dict or pandas DataFrame for time series input.")

        feature_names = self.schema.get("feature_names", [])
        missing = [f for f in feature_names if f not in df.columns]
        if missing:
            raise ValueError(f"Missing required time series features: {missing}. Expected: {feature_names}")

        X = df[feature_names]
        if self.preprocessor is not None:
            X_trans = self.preprocessor.transform(X)
        else:
            X_trans = X.values

        predictions = self.model.predict(X_trans)
        is_single = len(df) == 1
        pred_val = float(predictions[0]) if is_single else [float(x) for x in predictions]

        return {
            "prediction": pred_val,
            "task": "TIME_SERIES_FORECASTING"
        }
