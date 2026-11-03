import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from app.trainers.base_trainer import BaseTrainer
from app.services.schema_detector import SchemaDetector
from app.services.model_packager import ModelPackager
from app.services.model_validator import ModelValidator
from app.core.logging import logger

class TimeSeriesTrainer(BaseTrainer):
    """AutoML trainer for Time-Series forecasting with strict chronological split and lag feature engineering."""

    def __init__(self, job_id: str, dataset_path: Path, requirement: str, options: Optional[Dict[str, Any]] = None):
        super().__init__(job_id, dataset_path, requirement, options)
        self.time_col = None
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
        ext = data_file.suffix.lower()
        if ext == ".csv":
            df = pd.read_csv(data_file, nrows=50)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(data_file, nrows=50)
        elif ext == ".parquet":
            df = pd.read_parquet(data_file)[:50]
        else:
            df = pd.read_csv(data_file, nrows=50)
        return {
            "modality": "TIME_SERIES",
            "task": "TIME_SERIES_FORECASTING",
            "columns": list(df.columns)
        }

    def prepare_data(self) -> Dict[str, Any]:
        data_file = self._resolve_data_file()
        ext = data_file.suffix.lower()
        if ext == ".csv":
            df = pd.read_csv(data_file)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(data_file)
        elif ext == ".parquet":
            df = pd.read_parquet(data_file)
        else:
            df = pd.read_csv(data_file)

        # 1. Detect time column
        time_keywords = ["time", "date", "timestamp", "datetime", "day", "period"]
        for col in df.columns:
            if any(k in str(col).lower() for k in time_keywords):
                self.time_col = col
                break

        if not self.time_col:
            # Fallback to first column
            self.time_col = df.columns[0]

        # Convert to datetime and sort chronologically
        df[self.time_col] = pd.to_datetime(df[self.time_col], errors="coerce")
        df = df.dropna(subset=[self.time_col]).sort_values(self.time_col).reset_index(drop=True)

        self.data_processing_summary.append(f"Identified '{self.time_col}' as time index. Dataset strictly sorted in chronological order.")

        # 2. Detect target column (numerical metric to forecast)
        if not self.target_col or self.target_col not in df.columns:
            numeric_cols = [c for c in df.select_dtypes(include=np.number).columns if c != self.time_col]
            if numeric_cols:
                self.target_col = numeric_cols[-1]
            else:
                raise ValueError("No continuous numerical target column found in time series data.")

        # 3. Engineer Lag & Calendar Features
        engineered_df = pd.DataFrame()
        engineered_df[self.target_col] = df[self.target_col]

        # Datetime attributes
        dt_series = df[self.time_col].dt
        engineered_df["hour"] = dt_series.hour
        engineered_df["day_of_week"] = dt_series.dayofweek
        engineered_df["day_of_month"] = dt_series.day
        engineered_df["month"] = dt_series.month

        # Lag features (past 1, 2, 3 periods)
        for lag in [1, 2, 3]:
            engineered_df[f"{self.target_col}_lag_{lag}"] = df[self.target_col].shift(lag)

        # Rolling statistics
        engineered_df[f"{self.target_col}_rolling_mean_3"] = df[self.target_col].shift(1).rolling(window=3).mean()

        # Include other exogenous numerical columns if present
        for col in df.select_dtypes(include=np.number).columns:
            if col not in [self.time_col, self.target_col]:
                engineered_df[col] = df[col]

        # Drop rows with NaN caused by shifting
        initial_len = len(engineered_df)
        clean_df = engineered_df.dropna().reset_index(drop=True)
        dropped_lags = initial_len - len(clean_df)
        self.data_processing_summary.append(
            f"Constructed lag features (t-1, t-2, t-3), rolling 3-period mean, and temporal calendar features. "
            f"Initialized first {dropped_lags} lag windows."
        )

        y = clean_df[self.target_col]
        X = clean_df.drop(columns=[self.target_col])
        self.feature_names = list(X.columns)

        # 4. STRICT CHRONOLOGICAL SPLIT (No random shuffle!)
        test_ratio = float(self.options.get("test_size", 0.2))
        split_idx = int(len(clean_df) * (1.0 - test_ratio))

        X_train_df = X.iloc[:split_idx]
        X_test_df = X.iloc[split_idx:]
        y_train = y.iloc[:split_idx]
        y_test = y.iloc[split_idx:]

        self.data_processing_summary.append(
            f"Applied strict chronological split (First {len(X_train_df):,} periods for training, subsequent {len(X_test_df):,} periods for test). Zero future lookahead leakage."
        )

        self.X_train = X_train_df.values
        self.X_test = X_test_df.values
        self.y_train = y_train.values
        self.y_test = y_test.values

        self.test_df_sample = X_test_df.iloc[[0]].to_dict(orient="records")[0]

        self.schema = {
            "format": "timeseries",
            "feature_names": self.feature_names,
            "target": {"name": self.target_col, "type": "float"}
        }

        return {
            "total_samples": len(clean_df),
            "train_samples": len(X_train_df),
            "test_samples": len(X_test_df),
            "target_column": self.target_col,
            "features": self.feature_names
        }

    def recommend_models(self) -> List[Dict[str, Any]]:
        return [
            {"model_name": "gradient_boosting", "display_name": "Gradient Boosting Regressor", "is_recommended": True},
            {"model_name": "random_forest", "display_name": "Random Forest Regressor", "is_recommended": False}
        ]

    def train(self, progress_callback: Optional[Callable[[int, str, Optional[Dict[str, Any]]], None]] = None) -> Dict[str, Any]:
        candidates = {
            "Gradient Boosting": HistGradientBoostingRegressor(max_iter=100, random_state=42),
            "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
        }

        total = len(candidates)
        idx = 0

        for name, model in candidates.items():
            idx += 1
            pct = int(25 + (idx / total) * 50)
            if progress_callback:
                progress_callback(pct, f"Training time-series model {idx}/{total}: {name}", None)

            start_t = time.time()
            model.fit(self.X_train, self.y_train)
            dur = time.time() - start_t
            self.trained_models[name] = {"model": model, "train_time": round(dur, 3)}

        return self.evaluate()

    def evaluate(self) -> Dict[str, Any]:
        evaluations = {}
        for name, info in self.trained_models.items():
            model = info["model"]
            preds = model.predict(self.X_test)

            rmse = float(np.sqrt(mean_squared_error(self.y_test, preds)))
            mae = float(mean_absolute_error(self.y_test, preds))
            r2 = float(r2_score(self.y_test, preds))

            evaluations[name] = {
                "rmse": round(rmse, 4),
                "mae": round(mae, 4),
                "r2": round(r2, 4),
                "train_time_sec": info["train_time"],
                "primary_metric": round(-rmse, 4)
            }

        self.evaluations = evaluations
        return evaluations

    def select_best_model(self) -> Tuple[str, Any, Dict[str, Any]]:
        best_name = max(self.evaluations.items(), key=lambda x: x[1]["primary_metric"])[0]
        self.best_model_name = best_name
        self.best_model_obj = self.trained_models[best_name]["model"]
        return best_name, self.best_model_obj, self.evaluations[best_name]

    def package_model(self, output_dir: Path) -> Path:
        best_name, best_obj, best_metrics = self.select_best_model()
        model_clean_name = f"timeseries_forecast_{self.target_col}_{self.job_id[:8]}"
        out_file = output_dir / f"{model_clean_name}.aiforge"

        metadata = {
            "model_name": model_clean_name,
            "task": "TIME_SERIES_FORECASTING",
            "modality": "TIME_SERIES",
            "model_type": f"{best_name} (Autoregressive Lags)",
            "best_metric_name": "rmse",
            "best_metric_value": best_metrics["rmse"],
            "metrics": best_metrics,
            "target_column": self.target_col,
            "feature_names": self.feature_names,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        packaged_path = ModelPackager.package(
            output_filepath=out_file,
            model_obj=best_obj,
            preprocessor_obj=None,
            metadata=metadata,
            schema=self.schema,
            predictor_type="timeseries"
        )

        valid, msg, report = ModelValidator.validate_package(packaged_path, self.test_df_sample)
        if not valid:
            raise RuntimeError(f"Packaged time-series model validation failed: {msg}")

        return packaged_path
