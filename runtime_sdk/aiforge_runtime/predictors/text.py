from typing import Any, Dict, List, Union
import numpy as np
from .base import BasePredictor
from ..validators.schema import SchemaValidator

class TextPredictor(BasePredictor):
    def predict(self, input_data: Any) -> Dict[str, Any]:
        """
        Accepts:
            - Single text string
            - List of text strings
        """
        texts = SchemaValidator.validate_text(input_data)
        is_single = len(texts) == 1

        # Preprocess text (TF-IDF vectorizer)
        if self.preprocessor is not None:
            X_vec = self.preprocessor.transform(texts)
        else:
            X_vec = texts

        raw_pred = self.model.predict(X_vec)

        # Probabilities
        probabilities = None
        confidence = None

        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(X_vec)
            classes = list(self.model.classes_)

            if is_single:
                confidence = float(np.max(proba[0]))
                probabilities = {str(classes[i]): float(proba[0][i]) for i in range(len(classes))}
            else:
                confidence = [float(np.max(p)) for p in proba]
                probabilities = [
                    {str(classes[i]): float(p[i]) for i in range(len(classes))}
                    for p in proba
                ]
        elif hasattr(self.model, "decision_function"):
            # SVM margin distance converted to pseudo-probabilities via softmax
            df_vals = self.model.decision_function(X_vec)
            if df_vals.ndim == 1:
                # Binary classification
                exp_vals = np.exp(np.vstack([-df_vals, df_vals]).T)
            else:
                exp_vals = np.exp(df_vals)
            proba = exp_vals / np.sum(exp_vals, axis=1, keepdims=True)
            classes = list(self.model.classes_)
            if is_single:
                confidence = float(np.max(proba[0]))
                probabilities = {str(classes[i]): float(proba[0][i]) for i in range(len(classes))}
            else:
                confidence = [float(np.max(p)) for p in proba]
                probabilities = [
                    {str(classes[i]): float(p[i]) for i in range(len(classes))}
                    for p in proba
                ]

        pred_val = raw_pred[0] if is_single else raw_pred.tolist()
        if isinstance(pred_val, (np.integer, np.floating)):
            pred_val = pred_val.item()

        return {
            "prediction": str(pred_val),
            "confidence": round(confidence, 4) if isinstance(confidence, float) else confidence,
            "probabilities": probabilities,
            "task": "TEXT_CLASSIFICATION"
        }
