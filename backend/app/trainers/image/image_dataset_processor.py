import os
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
from PIL import Image
import pandas as pd
from app.core.logging import logger

VALID_IMG_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

class ImageDatasetProcessor:
    """Discovers, validates, and prepares image datasets from folders or CSV annotations."""

    @staticmethod
    def load_and_validate_dataset(
        path: Path
    ) -> Tuple[List[Tuple[Path, str]], List[str], Dict[str, Any]]:
        """
        Loads image samples and validates integrity.
        Returns:
            samples: List of (image_file_path, class_label)
            classes: List of unique class label names
            report: Stats on valid, corrupt, or excluded images
        """
        path = Path(path)
        samples = []
        corrupt_count = 0
        excluded_count = 0

        # Check if path is directory or archive
        if path.is_file() and path.suffix.lower() == ".zip":
            from app.core.security import safe_extract_zip
            extracted_dir = path.parent / f"extracted_{path.stem}"
            safe_extract_zip(path, extracted_dir)
            path = extracted_dir

        # Case 1: Folder with subdirectories as classes
        # e.g. path/cats/*.jpg, path/dogs/*.jpg
        subdirs = [d for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")]

        if len(subdirs) >= 2:
            for subdir in subdirs:
                class_name = subdir.name
                for f in subdir.rglob("*"):
                    if f.is_file() and f.suffix.lower() in VALID_IMG_EXTENSIONS:
                        # Validate PIL can open and verify image
                        try:
                            with Image.open(f) as img:
                                img.verify()
                            samples.append((f, class_name))
                        except Exception:
                            corrupt_count += 1
        else:
            # Case 2: Metadata CSV alongside images
            csv_files = [f for f in path.rglob("*.csv") if f.is_file()]
            if csv_files:
                df = pd.read_csv(csv_files[0])
                # Find image path column and label column
                img_col = None
                label_col = None
                for col in df.columns:
                    sample_vals = df[col].dropna().astype(str).head(5)
                    if any(any(s.lower().endswith(ext) for ext in VALID_IMG_EXTENSIONS) for s in sample_vals):
                        img_col = col
                    elif label_col is None:
                        label_col = col

                if img_col and label_col:
                    for _, row in df.iterrows():
                        img_rel = str(row[img_col])
                        label = str(row[label_col])
                        img_file = path / img_rel
                        if not img_file.exists():
                            # Search in subdirectories
                            matches = list(path.rglob(Path(img_rel).name))
                            if matches:
                                img_file = matches[0]

                        if img_file.exists():
                            try:
                                with Image.open(img_file) as img:
                                    img.verify()
                                samples.append((img_file, label))
                            except Exception:
                                corrupt_count += 1
                        else:
                            excluded_count += 1
            else:
                # Case 3: Flat folder with labels in filename (e.g. cat_001.jpg, dog_002.jpg)
                all_images = [f for f in path.rglob("*") if f.is_file() and f.suffix.lower() in VALID_IMG_EXTENSIONS]
                for f in all_images:
                    label = f.stem.split("_")[0] if "_" in f.stem else f.stem.split("-")[0]
                    try:
                        with Image.open(f) as img:
                            img.verify()
                        samples.append((f, label))
                    except Exception:
                        corrupt_count += 1

        classes = sorted(list({s[1] for s in samples}))

        report = {
            "total_discovered": len(samples) + corrupt_count + excluded_count,
            "valid_samples": len(samples),
            "corrupt_images": corrupt_count,
            "missing_images": excluded_count,
            "classes": classes,
            "num_classes": len(classes)
        }

        return samples, classes, report
