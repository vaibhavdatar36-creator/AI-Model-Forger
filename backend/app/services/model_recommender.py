from typing import Dict, Any, List, Optional
from app.schemas.responses import ModelCandidateRecommendation

class ModelRecommender:
    """Universal model recommender providing ranked candidate architectures and selection validation."""

    @staticmethod
    def recommend(
        modality: str,
        task: str,
        dataset_size_rows: int = 1000,
        hardware_info: Optional[Dict[str, Any]] = None
    ) -> List[ModelCandidateRecommendation]:
        recommendations = []
        has_gpu = hardware_info.get("cuda_available", False) if hardware_info else False

        if modality == "IMAGE" or task == "IMAGE_CLASSIFICATION":
            recommendations.append(ModelCandidateRecommendation(
                model_name="mobilenet_v2",
                display_name="MobileNetV2 (Transfer Learning)",
                is_recommended=True,
                suitability_score=0.96,
                reasons=[
                    "Highly efficient pretrained CNN architecture.",
                    "Fast convergence and low latency inference.",
                    "Excellent performance on small-to-medium visual datasets without overfitting."
                ],
                tradeoffs=["Slightly lower top-1 capacity than heavy Vision Transformers."]
            ))
            recommendations.append(ModelCandidateRecommendation(
                model_name="resnet18",
                display_name="ResNet18 (Residual Network)",
                is_recommended=False,
                suitability_score=0.92,
                reasons=[
                    "Deep residual connections prevent vanishing gradients.",
                    "Standard industrial baseline for computer vision."
                ],
                tradeoffs=["Higher compute and memory requirement than MobileNet."]
            ))
            recommendations.append(ModelCandidateRecommendation(
                model_name="custom_cnn",
                display_name="Lightweight Custom CNN",
                is_recommended=False,
                suitability_score=0.82,
                reasons=[
                    "Zero external pre-trained weight dependencies.",
                    "Very small package footprint."
                ],
                tradeoffs=["Requires larger datasets to achieve comparable accuracy."]
            ))
            return recommendations

        if modality == "TEXT" or task == "TEXT_CLASSIFICATION":
            recommendations.append(ModelCandidateRecommendation(
                model_name="tfidf_logistic_regression",
                display_name="TF-IDF + Logistic Regression",
                is_recommended=True,
                suitability_score=0.95,
                reasons=[
                    "Fast training, strong baseline performance on text classification.",
                    "Calibrated probability outputs for reliable confidence scoring.",
                    "Interpretable n-gram feature weights."
                ],
                tradeoffs=["Does not model deep sequential syntax like large language models."]
            ))
            recommendations.append(ModelCandidateRecommendation(
                model_name="tfidf_linear_svc",
                display_name="TF-IDF + Linear SVM",
                is_recommended=False,
                suitability_score=0.92,
                reasons=[
                    "Effective in high-dimensional sparse text vector spaces.",
                    "Robust margin-maximizing boundary."
                ],
                tradeoffs=["Requires calibration for class probabilities."]
            ))
            recommendations.append(ModelCandidateRecommendation(
                model_name="tfidf_naive_bayes",
                display_name="TF-IDF + Multinomial Naive Bayes",
                is_recommended=False,
                suitability_score=0.86,
                reasons=["Extremely fast training and lightweight memory footprint."],
                tradeoffs=["Assumes feature independence."]
            ))
            return recommendations

        if task == "TIME_SERIES_FORECASTING" or modality == "TIME_SERIES":
            recommendations.append(ModelCandidateRecommendation(
                model_name="timeseries_gradient_boosting",
                display_name="Lag-Feature Gradient Boosting Regressor",
                is_recommended=True,
                suitability_score=0.95,
                reasons=[
                    "Captures complex non-linear temporal trends and seasonal interactions.",
                    "Robust to outliers and scale variations.",
                    "Automatic feature interaction handling."
                ],
                tradeoffs=["Requires sufficient historical lag points."]
            ))
            recommendations.append(ModelCandidateRecommendation(
                model_name="timeseries_random_forest",
                display_name="Lag-Feature Random Forest Regressor",
                is_recommended=False,
                suitability_score=0.90,
                reasons=["Ensemble tree averaging provides stable forecasts."],
                tradeoffs=["Cannot extrapolate trends strictly beyond training bounds."]
            ))
            return recommendations

        if task == "TABULAR_REGRESSION":
            recommendations.append(ModelCandidateRecommendation(
                model_name="random_forest_regressor",
                display_name="Random Forest Regressor",
                is_recommended=True,
                suitability_score=0.95,
                reasons=[
                    "Nonlinear decision trees handle complex feature interactions.",
                    "Robust against outliers and collinear features.",
                    "Zero scale-sensitivity for trees."
                ],
                tradeoffs=["Model file can be larger for very deep trees."]
            ))
            recommendations.append(ModelCandidateRecommendation(
                model_name="hist_gradient_boosting_regressor",
                display_name="Histogram Gradient Boosting Regressor",
                is_recommended=False,
                suitability_score=0.93,
                reasons=["Extremely fast binning and native support for continuous values."],
                tradeoffs=["Requires hyperparameter tuning for small sample sizes."]
            ))
            recommendations.append(ModelCandidateRecommendation(
                model_name="ridge_regression",
                display_name="Ridge Linear Regressor (L2 Regularized)",
                is_recommended=False,
                suitability_score=0.82,
                reasons=["Highly interpretable coefficients with L2 penalty to curb overfitting."],
                tradeoffs=["Assumes linear relationships between features and target."]
            ))
            return recommendations

        # Default: TABULAR_CLASSIFICATION
        recommendations.append(ModelCandidateRecommendation(
            model_name="random_forest",
            display_name="Random Forest Classifier",
            is_recommended=True,
            suitability_score=0.96,
            reasons=[
                "Excels on tabular mixed numerical and categorical features.",
                "Inherent resistance to overfitting with bagging ensembles.",
                "Well-calibrated probability estimates."
            ],
            tradeoffs=["Slightly larger model package size."]
        ))
        recommendations.append(ModelCandidateRecommendation(
            model_name="hist_gradient_boosting",
            display_name="Histogram-based Gradient Boosting Classifier",
            is_recommended=False,
            suitability_score=0.94,
            reasons=[
                "High predictive accuracy via sequential gradient boosting.",
                "Fast training using binned histograms."
            ],
            tradeoffs=["Can be sensitive to noisy labels."]
        ))
        recommendations.append(ModelCandidateRecommendation(
            model_name="logistic_regression",
            display_name="Logistic Regression",
            is_recommended=False,
            suitability_score=0.85,
            reasons=["Fast, simple linear baseline with interpretable odds ratios."],
            tradeoffs=["Limited expressiveness on non-linear decision boundaries."]
        ))
        return recommendations

    @staticmethod
    def validate_user_selection(
        user_model: str,
        modality: str,
        task: str
    ) -> Dict[str, Any]:
        """Validates if user manual model selection is compatible with data modality and task."""
        m = modality.upper()
        t = task.upper()
        u = user_model.lower()

        # Mismatch checks
        if "regression" in u and "classification" in t:
            return {
                "valid": False,
                "message": f"'{user_model}' is a regression model, but your detected task is classification. Recommended: Random Forest Classifier or Gradient Boosting.",
                "suggested": "random_forest"
            }

        if any(term in u for term in ["linear", "ridge", "lasso", "logistic"]) and m == "IMAGE":
            return {
                "valid": False,
                "message": "Linear models are not suitable for raw image classification. Recommended: MobileNetV2 or CNN transfer learning.",
                "suggested": "mobilenet_v2"
            }

        return {"valid": True, "message": "Model choice is compatible with the detected task.", "suggested": user_model}
