import os
import unicodedata
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import pandas as pd
from app.core.logging import logger

class TextDatasetProcessor:
    """Discovers, normalizes, and cleans text classification datasets from files or folders."""

    @staticmethod
    def load_and_clean_text_dataset(
        path: Path,
        text_column: Optional[str] = None,
        label_column: Optional[str] = None
    ) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """
        Loads text dataset.
        Returns:
            texts: List of cleaned text strings
            labels: List of label strings
            report: Data cleaning report details
        """
        path = Path(path)
        texts = []
        labels = []
        empty_count = 0

        if path.is_dir():
            # Check for tabular text files (e.g. CSV in zip)
            csv_candidates = list(path.rglob("*.csv")) + list(path.rglob("*.jsonl"))
            subdirs = [d for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]
            if subdirs:
                # Subdirectories as classes
                for subdir in subdirs:
                    class_label = subdir.name
                    for txt_file in subdir.rglob("*.txt"):
                        if txt_file.is_file():
                            try:
                                content = txt_file.read_text(encoding="utf-8", errors="ignore").strip()
                                if content:
                                    texts.append(content)
                                    labels.append(class_label)
                                else:
                                    empty_count += 1
                            except Exception:
                                empty_count += 1
            elif csv_candidates:
                path = csv_candidates[0]

        if path.is_file():
            # File (CSV, JSONL, Parquet)
            ext = path.suffix.lower()
            if ext == ".csv":
                df = pd.read_csv(path)
            elif ext == ".jsonl":
                df = pd.read_json(path, lines=True)
            elif ext == ".parquet":
                df = pd.read_parquet(path)
            else:
                df = pd.read_csv(path)

            # Auto-detect text column and label column if not provided
            if not text_column or text_column not in df.columns:
                # Find column with highest average string length
                text_candidates = []
                for col in df.columns:
                    if df[col].dtype == object or str(df[col].dtype).startswith("string"):
                        avg_len = df[col].dropna().astype(str).map(len).mean()
                        text_candidates.append((col, avg_len))
                text_column = max(text_candidates, key=lambda x: x[1])[0] if text_candidates else df.columns[0]

            if not label_column or label_column not in df.columns:
                remaining_cols = [c for c in df.columns if c != text_column]
                label_column = remaining_cols[0] if remaining_cols else df.columns[-1]

            # Filter missing and clean
            initial_count = len(df)
            valid_df = df.dropna(subset=[text_column, label_column])
            empty_count = initial_count - len(valid_df)

            for _, row in valid_df.iterrows():
                raw_text = str(row[text_column]).strip()
                # Unicode normalization
                cleaned = unicodedata.normalize("NFKC", raw_text)
                if cleaned:
                    texts.append(cleaned)
                    labels.append(str(row[label_column]).strip())
                else:
                    empty_count += 1

        classes = sorted(list(set(labels)))
        report = {
            "total_samples": len(texts),
            "empty_records_removed": empty_count,
            "classes": classes,
            "num_classes": len(classes)
        }

        return texts, labels, report
