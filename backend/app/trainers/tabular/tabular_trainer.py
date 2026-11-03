import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error, mean_absolute_error, r2_score

from app.trainers.base_trainer import BaseTrainer
from app.services.dataset_profiler import DatasetProfiler
from app.services.data_engineer import TabularDataEngineer
from app.services.schema_detector import SchemaDetector
from app.services.model_packager import ModelPackager
from app.services.model_validator import ModelValidator
from app.utils.hardware import get_resource_aware_limits
from app.core.logging import logger

class TabularTrainer(BaseTrainer):
    """AutoML trainer for Tabular Classification and Regression."""

    def __init__(self, job_id: str, dataset_path: Path, requirement: str, options: Optional[Dict[str, Any]] = None):
        super().__init__(job_id, dataset_path, requirement, options)
        self.is_classification = True
        self.target_col = self.options.get("target_column")
        self.feature_names = []
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.test_df_sample = None

    def _resolve_data_file(self) -> Path:
        if self.dataset_path.is_file():
            return self.dataset_path
        if self.dataset_path.is_dir():
            for ext in [".csv", ".tsv", ".xlsx", ".xls", ".parquet", ".json"]:
                candidates = list(self.dataset_path.rglob(f"*{ext}"))
                if candidates:
                    return candidates[0]
        return self.dataset_path

    def analyze_dataset(self) -> Dict[str, Any]:
        data_file = self._resolve_data_file()
        profile = DatasetProfiler.profile(data_file, modality="TABULAR", requirement_target=self.target_col)
        if not self.target_col:
            self.target_col = profile.get("suggested_target")
        return profile

    def prepare_data(self) -> Dict[str, Any]:
        data_file = self._resolve_data_file()
        ext = data_file.suffix.lower()
        if ext == ".csv":
            df = pd.read_csv(data_file)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(data_file)
        elif ext == ".parquet":
            df = pd.read_parquet(data_file)
        elif ext == ".json":
            df = pd.read_json(data_file)
        else:
            df = pd.read_csv(data_file)

        if not self.target_col or self.target_col not in df.columns:
            self.target_col = df.columns[-1]

        # Profile dataset to identify IDs, constants, and types
        profile = DatasetProfiler.profile(data_file, modality="TABULAR", requirement_target=self.target_col)
        id_cols = profile.get("id_columns", [])
        constant_cols = profile.get("constant_columns", [])

        # Determine classification vs regression
        y_raw = df[self.target_col].dropna()
        is_num = pd.api.types.is_numeric_dtype(y_raw)
        distinct_count = y_raw.nunique()
        self.is_classification = not is_num or distinct_count <= 10

        # Memory / size sampling if dataset is huge (> 100k rows)
        resource_limits = get_resource_aware_limits(len(df))
        if resource_limits["tabular_sample_size"] and len(df) > resource_limits["tabular_sample_size"]:
            df = df.sample(n=resource_limits["tabular_sample_size"], random_state=42)
            self.data_processing_summary.append(f"Sampled {len(df):,} representative rows for efficient model comparison.")

        # Data engineering & pipeline creation
        preprocessor, feature_names, X, y, actions = TabularDataEngineer.prepare_tabular_pipeline(
            df=df,
            target_col=self.target_col,
            id_cols=id_cols,
            constant_cols=constant_cols
        )
        self.preprocessor = preprocessor
        self.feature_names = feature_names
        self.data_processing_summary.extend(actions)

        # Build schema
        self.schema = SchemaDetector.detect_tabular_schema(df, feature_names, self.target_col)

        # Train / Test split
        test_size = float(self.options.get("test_size", 0.2))
        random_seed = int(self.options.get("random_seed", 42))

        stratify = None
        if self.is_classification:
            # Check if all classes have at least 2 samples for stratified split
            class_counts = y.value_counts()
            if (class_counts >= 2).all():
                stratify = y

        X_train_df, X_test_df, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_seed, stratify=stratify
        )

        # Fit preprocessor on train only (no leakage!)
        X_train_trans = self.preprocessor.fit_transform(X_train_df)
        X_test_trans = self.preprocessor.transform(X_test_df)

        self.X_train = X_train_trans
        self.X_test = X_test_trans
        self.y_train = y_train
        self.y_test = y_test

        # Save single test sample for validation
        self.test_df_sample = X_test_df.iloc[[0]].to_dict(orient="records")[0]

        return {
            "total_samples": len(df),
            "train_samples": len(X_train_df),
            "test_samples": len(X_test_df),
            "features_count": len(feature_names),
            "is_classification": self.is_classification
        }

    def recommend_models(self) -> List[Dict[str, Any]]:
        task = "TABULAR_CLASSIFICATION" if self.is_classification else "TABULAR_REGRESSION"
        return [r.dict() for r in ModelRecommender.recommend("TABULAR", task)]

    def train(self, progress_callback: Optional[Callable[[int, str, Optional[Dict[str, Any]]], None]] = None) -> Dict[str, Any]:
        hw = get_resource_aware_limits(len(self.X_train))
        n_est = hw["tabular_n_estimators"]

        candidates = {}
        if self.is_classification:
            candidates["Random Forest"] = RandomForestClassifier(n_estimators=n_est, max_depth=12, random_state=42, n_jobs=-1)
            candidates["HistGradientBoosting"] = HistGradientBoostingClassifier(max_iter=n_est, random_state=42)
            candidates["Logistic Regression"] = LogisticRegression(max_iter=500, random_state=42)
        else:
            candidates["Random Forest"] = RandomForestRegressor(n_estimators=n_est, max_depth=12, random_state=42, n_jobs=-1)
            candidates["HistGradientBoosting"] = HistGradientBoostingRegressor(max_iter=n_est, random_state=42)
            candidates["Ridge Regression"] = Ridge(alpha=1.0, random_state=42)

        # Allow user model override
        user_choice = self.options.get("model_choice")
        if user_choice and user_choice != "auto":
            for name in list(candidates.keys()):
                if user_choice.lower() in name.lower().replace(" ", "_"):
                    candidates = {name: candidates[name]}
                    break

        total_candidates = len(candidates)
        idx = 0

        for name, model in candidates.items():
            idx += 1
            pct = int(20 + (idx / total_candidates) * 50)
            if progress_callback:
                progress_callback(pct, f"Training candidate model {idx}/{total_candidates}: {name}", None)

            start_t = time.time()
            model.fit(self.X_train, self.y_train)
            train_duration = time.time() - start_t
            self.trained_models[name] = {
                "model": model,
                "train_time": round(train_duration, 3)
            }

        return self.evaluate()

    def evaluate(self) -> Dict[str, Any]:
        evaluations = {}

        for name, info in self.trained_models.items():
            model = info["model"]
            preds = model.predict(self.X_test)

            if self.is_classification:
                acc = float(accuracy_score(self.y_test, preds))
                f1_macro = float(f1_score(self.y_test, preds, average="macro", zero_division=0))
                f1_weighted = float(f1_score(self.y_test, preds, average="weighted", zero_division=0))
                prec = float(precision_score(self.y_test, preds, average="weighted", zero_division=0))
                rec = float(recall_score(self.y_test, preds, average="weighted", zero_division=0))

                # Confusion matrix
                labels = [str(c) for c in np.unique(np.concatenate([self.y_test, preds]))]
                cm = confusion_matrix(self.y_test, preds, labels=labels).tolist()

                evaluations[name] = {
                    "accuracy": round(acc, 4),
                    "f1_macro": round(f1_macro, 4),
                    "f1_weighted": round(f1_weighted, 4),
                    "precision": round(prec, 4),
                    "recall": round(rec, 4),
                    "train_time_sec": info["train_time"],
                    "confusion_matrix": {"labels": labels, "matrix": cm},
                    "primary_metric": round(f1_macro, 4)
                }
            else: # Regression
                rmse = float(np.sqrt(mean_squared_error(self.y_test, preds)))
                mae = float(mean_absolute_error(self.y_test, preds))
                r2 = float(r2_score(self.y_test, preds))

                evaluations[name] = {
                    "rmse": round(rmse, 4),
                    "mae": round(mae, 4),
                    "r2": round(r2, 4),
                    "train_time_sec": info["train_time"],
                    "primary_metric": round(-rmse, 4) # Higher is better
                }

        self.evaluations = evaluations
        return evaluations

    def select_best_model(self) -> Tuple[str, Any, Dict[str, Any]]:
        if not self.evaluations:
            self.evaluate()

        best_name = max(self.evaluations.items(), key=lambda x: x[1]["primary_metric"])[0]
        self.best_model_name = best_name
        self.best_model_obj = self.trained_models[best_name]["model"]
        return best_name, self.best_model_obj, self.evaluations[best_name]

    def package_model(self, output_dir: Path) -> Path:
        best_name, best_obj, best_metrics = self.select_best_model()
        task = "TABULAR_CLASSIFICATION" if self.is_classification else "TABULAR_REGRESSION"
        primary_metric_name = "f1_macro" if self.is_classification else "rmse"
        primary_metric_val = best_metrics.get("f1_macro") if self.is_classification else best_metrics.get("rmse")

        model_clean_name = f"{self.target_col}_{task.lower()}"
        out_file = output_dir / f"{model_clean_name}.aiforge"

        metadata = {
            "model_name": model_clean_name,
            "task": task,
            "modality": "TABULAR",
            "model_type": best_name,
            "best_metric_name": primary_metric_name,
            "best_metric_value": primary_metric_val,
            "metrics": best_metrics,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "feature_names": self.feature_names,
            "target_column": self.target_col
        }

        packaged_path = ModelPackager.package(
            output_filepath=out_file,
            model_obj=best_obj,
            preprocessor_obj=self.preprocessor,
            metadata=metadata,
            schema=self.schema,
            predictor_type="tabular"
        )

        # Validate package before download release
        valid, msg, report = ModelValidator.validate_package(packaged_path, self.test_df_sample)
        if not valid:
            raise RuntimeError(f"Packaged model validation failed: {msg}")

        return packaged_path
