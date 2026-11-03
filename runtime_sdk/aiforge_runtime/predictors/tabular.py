from typing import Any, Dict, List
import numpy as np
import pandas as pd
from .base import BasePredictor
from ..validators.schema import SchemaValidator

class TabularPredictor(BasePredictor):
    def predict(self, input_data: Any) -> Dict[str, Any]:
        df = SchemaValidator.validate_tabular(input_data, self.schema)
        task = self.metadata.get("task", "TABULAR_CLASSIFICATION")

        # Apply preprocessing
        if self.preprocessor is not None:
            X_trans = self.preprocessor.transform(df)
        else:
            X_trans = df.values

        # Predictions
        raw_pred = self.model.predict(X_trans)

        is_single = len(df) == 1

        if "CLASSIFICATION" in task:
            probabilities = None
            confidence = None

            if hasattr(self.model, "predict_proba"):
                proba = self.model.predict_proba(X_trans)
                classes = list(self.model.classes_)

                if is_single:
                    prob_dict = {str(classes[i]): float(proba[0][i]) for i in range(len(classes))}
                    confidence = float(np.max(proba[0]))
                    probabilities = prob_dict
                else:
                    probabilities = [
                        {str(classes[i]): float(p[i]) for i in range(len(classes))}
                        for p in proba
                    ]
                    confidence = [float(np.max(p)) for p in proba]

            prediction_val = raw_pred[0] if is_single else raw_pred.tolist()
            # Convert numpy types to native python
            if isinstance(prediction_val, (np.integer, np.floating)):
                prediction_val = prediction_val.item()

            return {
                "prediction": prediction_val,
                "confidence": confidence,
                "probabilities": probabilities,
                "task": task
            }
        else: # REGRESSION
            prediction_val = float(raw_pred[0]) if is_single else [float(x) for x in raw_pred]
            return {
                "prediction": prediction_val,
                "task": task
            }
