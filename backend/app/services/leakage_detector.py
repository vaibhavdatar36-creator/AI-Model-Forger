from typing import List, Dict, Any
import pandas as pd
import numpy as np
from app.core.logging import logger

class LeakageDetector:
    """Detects target leakage and identity features that artificially inflate model performance."""

    @staticmethod
    def detect_leakage(df: pd.DataFrame, target_col: str) -> List[Dict[str, Any]]:
        leakage_suspects = []
        if target_col not in df.columns or len(df) < 10:
            return leakage_suspects

        target_series = df[target_col]
        
        for col in df.columns:
            if col == target_col:
                continue
                
            series = df[col]

            # 1. Exact match / identical column
            if series.equals(target_series):
                leakage_suspects.append({
                    "column": col,
                    "reason": "Column values are 100% identical to target column (direct leakage).",
                    "severity": "CRITICAL"
                })
                continue

            # 2. Perfect or near-perfect Pearson/Spearman correlation for numeric
            if pd.api.types.is_numeric_dtype(series) and pd.api.types.is_numeric_dtype(target_series):
                corr = series.corr(target_series)
                if abs(corr) >= 0.99:
                    leakage_suspects.append({
                        "column": col,
                        "reason": f"Extreme correlation with target (|r| = {abs(corr):.4f}). Likely target derivative or post-outcome metric.",
                        "severity": "HIGH"
                    })
                    
        return leakage_suspects
