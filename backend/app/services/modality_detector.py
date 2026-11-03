import os
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
import pandas as pd
from app.core.logging import logger

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".doc"}
TEXT_EXTENSIONS = {".txt", ".jsonl"}
TABULAR_EXTENSIONS = {".csv", ".tsv", ".xlsx", ".xls", ".parquet"}

class ModalityDetector:
    """Inspects files, archives, and directories to determine dataset modality with confidence."""

    @staticmethod
    def detect(file_or_dir_path: Path) -> Dict[str, Any]:
        path = Path(file_or_dir_path)
        if not path.exists():
            return {
                "modality": "UNKNOWN",
                "confidence": 0.0,
                "reasons": [f"File or directory does not exist: {path}"],
                "details": {}
            }

        # Case 1: Directory
        if path.is_dir():
            return ModalityDetector._detect_directory(path)

        # Case 2: Archive (.zip)
        if path.suffix.lower() == ".zip":
            # For archives that have already been extracted or need directory inspection
            extracted_dir = path.parent / f"extracted_{path.stem}"
            if extracted_dir.exists() and extracted_dir.is_dir():
                return ModalityDetector._detect_directory(extracted_dir)
            # If not yet extracted, peek into zip structure
            import zipfile
            try:
                with zipfile.ZipFile(path, 'r') as zf:
                    names = zf.namelist()
                    exts = [Path(n).suffix.lower() for n in names if not n.endswith("/")]
                    img_count = sum(1 for e in exts if e in IMAGE_EXTENSIONS)
                    txt_count = sum(1 for e in exts if e in TEXT_EXTENSIONS)
                    audio_count = sum(1 for e in exts if e in AUDIO_EXTENSIONS)
                    video_count = sum(1 for e in exts if e in VIDEO_EXTENSIONS)
                    tab_count = sum(1 for e in exts if e in TABULAR_EXTENSIONS)

                    total_files = len(exts) or 1
                    if img_count / total_files > 0.4:
                        return {
                            "modality": "IMAGE",
                            "confidence": 0.95,
                            "reasons": [f"Archive contains {img_count} images in structured folders"],
                            "details": {"image_count": img_count, "total_files": total_files}
                        }
                    if txt_count / total_files > 0.4:
                        return {
                            "modality": "TEXT",
                            "confidence": 0.92,
                            "reasons": [f"Archive contains {txt_count} text files"],
                            "details": {"text_count": txt_count, "total_files": total_files}
                        }
                    if audio_count > 0:
                        return {
                            "modality": "AUDIO",
                            "confidence": 0.95,
                            "reasons": [f"Archive contains {audio_count} audio files"],
                            "details": {"audio_count": audio_count}
                        }
                    if video_count > 0:
                        return {
                            "modality": "VIDEO",
                            "confidence": 0.95,
                            "reasons": [f"Archive contains {video_count} video files"],
                            "details": {"video_count": video_count}
                        }
            except Exception as e:
                logger.warning(f"Error inspecting zip: {e}")

        # Case 3: Single file inspection
        ext = path.suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            return {
                "modality": "IMAGE",
                "confidence": 0.98,
                "reasons": [f"Single image file with extension {ext}"],
                "details": {"extension": ext}
            }

        if ext in AUDIO_EXTENSIONS:
            return {
                "modality": "AUDIO",
                "confidence": 0.98,
                "reasons": [f"Audio file with extension {ext}"],
                "details": {"extension": ext}
            }

        if ext in VIDEO_EXTENSIONS:
            return {
                "modality": "VIDEO",
                "confidence": 0.98,
                "reasons": [f"Video file with extension {ext}"],
                "details": {"extension": ext}
            }

        if ext in DOCUMENT_EXTENSIONS:
            return {
                "modality": "DOCUMENT",
                "confidence": 0.95,
                "reasons": [f"Document file with extension {ext}"],
                "details": {"extension": ext}
            }

        if ext == ".txt":
            return {
                "modality": "TEXT",
                "confidence": 0.90,
                "reasons": ["Plain text document file"],
                "details": {"extension": ext}
            }

        # Tabular / Structured (.csv, .xlsx, .json, .parquet)
        if ext in TABULAR_EXTENSIONS or ext == ".json":
            return ModalityDetector._detect_tabular_or_specialized(path)

        return {
            "modality": "UNKNOWN",
            "confidence": 0.3,
            "reasons": [f"Unrecognized file format: {ext}"],
            "details": {"extension": ext}
        }

    @staticmethod
    def _detect_directory(dir_path: Path) -> Dict[str, Any]:
        all_files = [f for f in dir_path.rglob("*") if f.is_file() and not f.name.startswith(".")]
        if not all_files:
            return {
                "modality": "UNKNOWN",
                "confidence": 0.0,
                "reasons": ["Directory is empty"],
                "details": {}
            }

        exts = [f.suffix.lower() for f in all_files]
        img_count = sum(1 for e in exts if e in IMAGE_EXTENSIONS)
        txt_count = sum(1 for e in exts if e in TEXT_EXTENSIONS)
        tab_count = sum(1 for e in exts if e in TABULAR_EXTENSIONS)
        audio_count = sum(1 for e in exts if e in AUDIO_EXTENSIONS)
        video_count = sum(1 for e in exts if e in VIDEO_EXTENSIONS)
        doc_count = sum(1 for e in exts if e in DOCUMENT_EXTENSIONS)
        total = len(all_files)

        if img_count / total >= 0.5:
            # Check subfolder structure for labels (e.g. dir/cat/1.jpg, dir/dog/2.jpg)
            subdirs = [d for d in dir_path.iterdir() if d.is_dir() and not d.name.startswith(".")]
            has_class_folders = len(subdirs) >= 2
            return {
                "modality": "IMAGE",
                "confidence": 0.97 if has_class_folders else 0.90,
                "reasons": [
                    f"Directory contains {img_count} images out of {total} files.",
                    f"Class subfolder organization: {len(subdirs)} classes detected." if has_class_folders else "Flat image folder."
                ],
                "details": {"image_count": img_count, "classes": [d.name for d in subdirs[:10]]}
            }

        if audio_count / total >= 0.5:
            return {
                "modality": "AUDIO",
                "confidence": 0.95,
                "reasons": [f"Directory contains {audio_count} audio files."],
                "details": {"audio_count": audio_count}
            }

        if video_count / total >= 0.5:
            return {
                "modality": "VIDEO",
                "confidence": 0.95,
                "reasons": [f"Directory contains {video_count} video files."],
                "details": {"video_count": video_count}
            }

        if txt_count / total >= 0.5:
            return {
                "modality": "TEXT",
                "confidence": 0.92,
                "reasons": [f"Directory contains {txt_count} text files."],
                "details": {"text_count": txt_count}
            }

        # Check for single tabular file with accompanying folder
        csv_files = [f for f in all_files if f.suffix.lower() == ".csv"]
        if csv_files and img_count > 0:
            return {
                "modality": "IMAGE",
                "confidence": 0.93,
                "reasons": [f"Found CSV metadata alongside {img_count} image files (Image Dataset with annotations)."],
                "details": {"csv_metadata": csv_files[0].name, "image_count": img_count}
            }

        return {
            "modality": "TABULAR" if tab_count > 0 else "UNKNOWN",
            "confidence": 0.75 if tab_count > 0 else 0.4,
            "reasons": [f"Mixed directory containing {total} files ({img_count} images, {tab_count} tables, {txt_count} texts)."],
            "details": {"total": total}
        }

    @staticmethod
    def _detect_tabular_or_specialized(file_path: Path) -> Dict[str, Any]:
        """Deep inspect tabular contents: checks if it's text NLP, time-series, image metadata, or standard tabular."""
        try:
            df = None
            ext = file_path.suffix.lower()
            if ext == ".csv":
                df = pd.read_csv(file_path, nrows=50)
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path, nrows=50)
            elif ext == ".parquet":
                df = pd.read_parquet(file_path)[:50]
            elif ext == ".json":
                df = pd.read_json(file_path, nrows=50)
        except Exception as e:
            return {
                "modality": "TABULAR",
                "confidence": 0.70,
                "reasons": [f"Tabular format file {ext}, but sample read encountered warning: {str(e)}"],
                "details": {}
            }

        if df is None or df.empty:
            return {
                "modality": "TABULAR",
                "confidence": 0.80,
                "reasons": ["Empty tabular dataset"],
                "details": {}
            }

        cols = [str(c).lower() for c in df.columns]

        # Check for image paths in columns (IMAGE_DATASET_WITH_METADATA)
        for col in df.columns:
            sample_vals = df[col].dropna().astype(str).head(10)
            has_image_paths = any(any(s.lower().endswith(ie) for ie in IMAGE_EXTENSIONS) for s in sample_vals)
            if has_image_paths:
                return {
                    "modality": "IMAGE",
                    "confidence": 0.94,
                    "reasons": [f"Column '{col}' contains image file references. Interpreting as Image Dataset with labels."],
                    "details": {"image_column": col, "columns": list(df.columns)}
                }

        # Check for prominent text classification dataset (e.g. text/review/comment/message/sentence column)
        text_cols = []
        for col in df.columns:
            if df[col].dtype == object or str(df[col].dtype).startswith("string"):
                avg_len = df[col].dropna().astype(str).map(len).mean()
                if avg_len > 40: # Substantial natural language sentences/paragraphs
                    text_cols.append((col, avg_len))
        
        # If there's 1-2 major text columns and few total columns (<= 4), likely TEXT NLP dataset
        if text_cols and len(df.columns) <= 5:
            best_text_col, avg_l = max(text_cols, key=lambda x: x[1])
            return {
                "modality": "TEXT",
                "confidence": 0.91,
                "reasons": [
                    f"Column '{best_text_col}' contains natural language text (avg length {avg_l:.1f} chars).",
                    "Dataset is structured for Text Classification / NLP."
                ],
                "details": {"text_column": best_text_col, "columns": list(df.columns)}
            }

        # Check for time-series: timestamp column + continuous metric
        time_exact_keywords = ["timestamp", "datetime", "date", "time", "hour", "year"]
        time_candidates = []
        for col in df.columns:
            c_lower = str(col).lower()
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                time_candidates.append(col)
            elif any(c_lower == tk or c_lower.endswith(f"_{tk}") or c_lower.startswith(f"{tk}_") for tk in time_exact_keywords):
                # Verify sample values parse as datetime
                try:
                    parsed = pd.to_datetime(df[col].dropna().head(10), errors="coerce")
                    if parsed.notna().sum() >= 5:
                        time_candidates.append(col)
                except Exception:
                    pass
        
        if time_candidates:
            return {
                "modality": "TIME_SERIES",
                "confidence": 0.90,
                "reasons": [f"Detected valid temporal column '{time_candidates[0]}' with sequential timestamp values."],
                "details": {"time_candidates": time_candidates}
            }

        # Standard Tabular
        return {
            "modality": "TABULAR",
            "confidence": 0.96,
            "reasons": [
                f"Structured tabular dataset with {len(df.columns)} features.",
                f"Contains numerical ({sum(1 for c in df.select_dtypes(include='number').columns)}) and categorical ({sum(1 for c in df.select_dtypes(exclude='number').columns)}) columns."
            ],
            "details": {"num_columns": len(df.columns), "columns": list(df.columns)}
        }
