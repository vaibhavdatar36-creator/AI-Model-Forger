import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from app.trainers.base_trainer import BaseTrainer
from app.trainers.text.text_dataset_processor import TextDatasetProcessor
from app.services.schema_detector import SchemaDetector
from app.services.model_packager import ModelPackager
from app.services.model_validator import ModelValidator
from app.core.logging import logger

class TextTrainer(BaseTrainer):
    """AutoML trainer for Natural Language Processing and Text Classification."""

    def __init__(self, job_id: str, dataset_path: Path, requirement: str, options: Optional[Dict[str, Any]] = None):
        super().__init__(job_id, dataset_path, requirement, options)
        self.texts = []
        self.labels = []
        self.classes = []
        self.vectorizer = None
        self.X_train_vec = None
        self.X_test_vec = None
        self.y_train = None
        self.y_test = None
        self.test_sample_text = None

    def analyze_dataset(self) -> Dict[str, Any]:
        texts, labels, report = TextDatasetProcessor.load_and_clean_text_dataset(self.dataset_path)
        return {
            "modality": "TEXT",
            "task": "TEXT_CLASSIFICATION",
            "total_samples": len(texts),
            "classes": report["classes"],
            "empty_removed": report["empty_records_removed"]
        }

    def prepare_data(self) -> Dict[str, Any]:
        texts, labels, report = TextDatasetProcessor.load_and_clean_text_dataset(
            self.dataset_path,
            text_column=self.options.get("text_column"),
            label_column=self.options.get("target_column")
        )

        if len(texts) < 4:
            raise ValueError(f"Insufficient text records for training. Found {len(texts)} samples.")

        self.texts = texts
        self.labels = labels
        self.classes = report["classes"]

        self.data_processing_summary.append(f"Loaded {len(texts):,} text samples across {len(self.classes)} classes.")
        if report["empty_records_removed"] > 0:
            self.data_processing_summary.append(f"Removed {report['empty_records_removed']:,} empty/whitespace records.")

        # Train / Test split
        test_size = float(self.options.get("test_size", 0.2))
        random_seed = int(self.options.get("random_seed", 42))

        # Check stratification
        unique_lbls, counts = np.unique(labels, return_counts=True)
        can_stratify = (counts >= 2).all()

        X_train_raw, X_test_raw, y_train, y_test = train_test_split(
            texts, labels,
            test_size=test_size,
            random_state=random_seed,
            stratify=labels if can_stratify else None
        )

        self.test_sample_text = X_test_raw[0]

        # TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=25000,
            sublinear_tf=True
        )

        # Fit on train text only
        self.X_train_vec = self.vectorizer.fit_transform(X_train_raw)
        self.X_test_vec = self.vectorizer.transform(X_test_raw)
        self.y_train = np.array(y_train)
        self.y_test = np.array(y_test)

        self.data_processing_summary.append(
            f"Configured TF-IDF vectorizer (unigrams + bigrams, vocab size {len(self.vectorizer.vocabulary_):,})."
        )

        self.schema = SchemaDetector.detect_text_schema(classes=self.classes)

        return {
            "total_samples": len(texts),
            "train_samples": len(X_train_raw),
            "test_samples": len(X_test_raw),
            "classes": self.classes
        }

    def recommend_models(self) -> List[Dict[str, Any]]:
        return [
            {"model_name": "tfidf_logistic_regression", "display_name": "TF-IDF + Logistic Regression", "is_recommended": True},
            {"model_name": "tfidf_linear_svc", "display_name": "TF-IDF + Linear SVM", "is_recommended": False},
            {"model_name": "tfidf_naive_bayes", "display_name": "TF-IDF + Multinomial Naive Bayes", "is_recommended": False}
        ]

    def train(self, progress_callback: Optional[Callable[[int, str, Optional[Dict[str, Any]]], None]] = None) -> Dict[str, Any]:
        candidates = {
            "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
            "Linear SVM": LinearSVC(random_state=42, dual=False),
            "Multinomial Naive Bayes": MultinomialNB()
        }

        user_choice = self.options.get("model_choice")
        if user_choice and user_choice != "auto":
            for name in list(candidates.keys()):
                if user_choice.lower() in name.lower().replace(" ", "_"):
                    candidates = {name: candidates[name]}
                    break

        total = len(candidates)
        idx = 0

        for name, model in candidates.items():
            idx += 1
            pct = int(25 + (idx / total) * 45)
            if progress_callback:
                progress_callback(pct, f"Training NLP model {idx}/{total}: {name}", None)

            start_t = time.time()
            model.fit(self.X_train_vec, self.y_train)
            dur = time.time() - start_t
            self.trained_models[name] = {"model": model, "train_time": round(dur, 3)}

        return self.evaluate()

    def evaluate(self) -> Dict[str, Any]:
        evaluations = {}
        for name, info in self.trained_models.items():
            model = info["model"]
            preds = model.predict(self.X_test_vec)

            acc = float(accuracy_score(self.y_test, preds))
            f1_macro = float(f1_score(self.y_test, preds, average="macro", zero_division=0))
            f1_weighted = float(f1_score(self.y_test, preds, average="weighted", zero_division=0))
            prec = float(precision_score(self.y_test, preds, average="weighted", zero_division=0))
            rec = float(recall_score(self.y_test, preds, average="weighted", zero_division=0))

            cm = confusion_matrix(self.y_test, preds, labels=self.classes).tolist()

            evaluations[name] = {
                "accuracy": round(acc, 4),
                "f1_macro": round(f1_macro, 4),
                "f1_weighted": round(f1_weighted, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "train_time_sec": info["train_time"],
                "confusion_matrix": {"labels": self.classes, "matrix": cm},
                "primary_metric": round(f1_macro, 4)
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
        model_clean_name = f"text_classifier_{self.job_id[:8]}"
        out_file = output_dir / f"{model_clean_name}.aiforge"

        metadata = {
            "model_name": model_clean_name,
            "task": "TEXT_CLASSIFICATION",
            "modality": "TEXT",
            "model_type": f"{best_name} (TF-IDF)",
            "best_metric_name": "f1_macro",
            "best_metric_value": best_metrics["f1_macro"],
            "metrics": best_metrics,
            "classes": self.classes,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        packaged_path = ModelPackager.package(
            output_filepath=out_file,
            model_obj=best_obj,
            preprocessor_obj=self.vectorizer,
            metadata=metadata,
            schema=self.schema,
            predictor_type="text"
        )

        valid, msg, report = ModelValidator.validate_package(packaged_path, self.test_sample_text)
        if not valid:
            raise RuntimeError(f"Packaged text model validation failed: {msg}")

        return packaged_path
