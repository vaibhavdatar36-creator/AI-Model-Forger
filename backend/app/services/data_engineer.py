from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from app.core.logging import logger

class TabularDataEngineer:
    """Automated tabular data cleaning, feature selection, and sklearn preprocessing pipeline."""

    @staticmethod
    def prepare_tabular_pipeline(
        df: pd.DataFrame,
        target_col: str,
        id_cols: Optional[List[str]] = None,
        constant_cols: Optional[List[str]] = None
    ) -> Tuple[ColumnTransformer, List[str], pd.DataFrame, pd.Series, List[str]]:
        """
        Cleans data and builds a full scikit-learn preprocessing ColumnTransformer.
        Returns:
            preprocessor, feature_names, X, y, report_actions
        """
        report_actions = []
        df = df.copy()

        # 1. Drop duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        dupes_removed = initial_count - len(df)
        if dupes_removed > 0:
            report_actions.append(f"Removed {dupes_removed:,} duplicate records.")

        # 2. Check target presence and drop rows with missing target
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataset.")

        missing_targets = int(df[target_col].isna().sum())
        if missing_targets > 0:
            df = df.dropna(subset=[target_col])
            report_actions.append(f"Excluded {missing_targets:,} rows with missing target '{target_col}'.")

        y = df[target_col]
        X = df.drop(columns=[target_col])

        # 3. Exclude ID, constant, and leakage columns
        exclude_cols = set(id_cols or []) | set(constant_cols or [])
        valid_feature_cols = [c for c in X.columns if c not in exclude_cols]

        if exclude_cols:
            report_actions.append(f"Excluded {len(exclude_cols)} ID/constant columns: {list(exclude_cols)}.")

        X = X[valid_feature_cols]

        # 4. Identify numerical and categorical columns
        numeric_features = []
        categorical_features = []

        for col in valid_feature_cols:
            if pd.api.types.is_numeric_dtype(X[col]):
                numeric_features.append(col)
            else:
                categorical_features.append(col)

        # 5. Build transformers
        transformers = []

        if numeric_features:
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            transformers.append(('num', numeric_transformer, numeric_features))
            report_actions.append(f"Applied median imputation and standard scaling to {len(numeric_features)} numerical features.")

        if categorical_features:
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])
            transformers.append(('cat', categorical_transformer, categorical_features))
            report_actions.append(f"Applied most-frequent imputation and robust One-Hot Encoding to {len(categorical_features)} categorical features.")

        preprocessor = ColumnTransformer(transformers=transformers, remainder='drop')

        total_missing = int(X.isna().sum().sum())
        if total_missing > 0:
            report_actions.append(f"Automatically handled {total_missing:,} missing values across features.")

        return preprocessor, valid_feature_cols, X, y, report_actions
