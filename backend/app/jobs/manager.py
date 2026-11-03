import os
import time
import uuid
import threading
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import logger
from app.core.path_resolver import resolve_dataset_path
from app.database.database import SessionLocal
from app.database.models import TrainingJob, ModelArtifact, Dataset, Project
from app.services.model_registry import TrainerRegistry
from app.services.modality_detector import ModalityDetector
from app.services.requirement_analyzer import RequirementAnalyzer
from app.services.task_detector import TaskDetector
from app.services.dataset_profiler import DatasetProfiler
from app.services.model_recommender import ModelRecommender

class JobManager:
    """Orchestrates asynchronous AutoML training workflows in background threads."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(JobManager, cls).__new__(cls)
                cls._instance._init_manager()
            return cls._instance

    def _init_manager(self):
        self.active_jobs: Dict[str, Dict[str, Any]] = {}

    def start_training_job(
        self,
        dataset_id: str,
        requirement: str,
        project_name: str = "AI Model Forge Project",
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        job_id = str(uuid.uuid4())
        project_id = str(uuid.uuid4())

        # Initialize job in database
        db = SessionLocal()
        try:
            # Check or create project
            proj = Project(id=project_id, name=project_name, requirement=requirement)
            db.add(proj)

            # Check dataset
            dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
            if not dataset:
                raise ValueError(f"Dataset {dataset_id} not found in database.")

            job = TrainingJob(
                id=job_id,
                project_id=project_id,
                dataset_id=dataset_id,
                status="ANALYZING",
                progress=5,
                current_step="Analyzing dataset and requirement",
                logs=f"[{datetime.utcnow().strftime('%H:%M:%S')}] Job initialized.\n"
            )
            db.add(job)
            db.commit()
        finally:
            db.close()

        # In-memory tracking
        self.active_jobs[job_id] = {
            "status": "ANALYZING",
            "progress": 5,
            "current_step": "Analyzing dataset and requirement",
            "logs": [f"[{datetime.utcnow().strftime('%H:%M:%S')}] Job initialized."],
            "result": None,
            "error": None
        }

        # Spawn background thread
        thread = threading.Thread(
            target=self._run_pipeline,
            args=(job_id, dataset_id, requirement, options or {}),
            daemon=True
        )
        thread.start()
        return job_id

    def _append_log(self, job_id: str, message: str, db: Optional[Session] = None):
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        logger.info(f"[{job_id[:8]}] {message}")

        if job_id in self.active_jobs:
            self.active_jobs[job_id]["logs"].append(log_entry)

        if db:
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            if job:
                job.logs = (job.logs or "") + log_entry + "\n"
                db.commit()

    def _update_status(self, job_id: str, status: str, progress: int, step: str, db: Session):
        if job_id in self.active_jobs:
            self.active_jobs[job_id]["status"] = status
            self.active_jobs[job_id]["progress"] = progress
            self.active_jobs[job_id]["current_step"] = step

        job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
        if job:
            job.status = status
            job.progress = progress
            job.current_step = step
            job.updated_at = datetime.utcnow()
            db.commit()

    def _run_pipeline(self, job_id: str, dataset_id: str, requirement: str, options: Dict[str, Any]):
        db = SessionLocal()
        start_time = time.time()
        try:
            dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
            dataset_path = Path(dataset.filepath)

            # Resolve if dataset path points to an extracted directory containing tabular data
            resolved_path = resolve_dataset_path(dataset_path, modality=options.get("modality"))
            if resolved_path != dataset_path and resolved_path.is_file():
                dataset.filepath = str(resolved_path)
                db.commit()
                dataset_path = resolved_path

            # Step 1: Dataset Modality & Requirement Analysis
            self._update_status(job_id, "ANALYZING", 10, "Determining dataset modality and natural language requirement", db)
            self._append_log(job_id, "Starting automatic dataset understanding...", db)

            req_analyzer = RequirementAnalyzer()
            req_analysis = req_analyzer.analyze(requirement)
            self._append_log(job_id, f"Requirement Objective: '{requirement}'", db)

            modality_info = ModalityDetector.detect(dataset_path)
            detected_modality = options.get("modality") or modality_info["modality"]
            self._append_log(job_id, f"Detected Modality: {detected_modality} (Confidence: {modality_info['confidence']*100:.1f}%)", db)

            # Step 2: Task Detection
            self._update_status(job_id, "ANALYZING", 20, "Detecting target ML/DL task", db)
            dataset_profile = DatasetProfiler.profile(dataset_path, modality=detected_modality)
            
            task_info = TaskDetector.detect(
                modality=detected_modality,
                requirement_analysis=req_analysis,
                dataset_profile=dataset_profile,
                target_column=options.get("target_column")
            )

            if not task_info["is_supported"]:
                raise RuntimeError(task_info["reason"])

            detected_task = options.get("task") or task_info["task"]
            self._append_log(job_id, f"Detected Task: {detected_task} (Confidence: {task_info['confidence']*100:.1f}%) - {task_info['reason']}", db)

            # Step 3: Instantiate Trainer
            trainer_cls = TrainerRegistry.get(detected_task)
            trainer = trainer_cls(
                job_id=job_id,
                dataset_path=dataset_path,
                requirement=requirement,
                options=options
            )

            # Step 4: Preprocessing Data
            self._update_status(job_id, "PREPROCESSING", 30, "Cleaning and preprocessing raw dataset", db)
            self._append_log(job_id, "Executing automatic data engineering and feature pipelines...", db)
            
            prep_stats = trainer.prepare_data()
            for summary_item in trainer.data_processing_summary:
                self._append_log(job_id, f"✓ {summary_item}", db)

            # Step 5: Training
            self._update_status(job_id, "TRAINING", 45, "Training candidate models", db)
            self._append_log(job_id, "Training candidate models with resource-aware settings...", db)

            def progress_cb(pct, msg, extra):
                self._update_status(job_id, "TRAINING", pct, msg, db)
                self._append_log(job_id, msg, db)

            evaluations = trainer.train(progress_callback=progress_cb)

            # Step 6: Evaluation & Selection
            self._update_status(job_id, "EVALUATING", 80, "Evaluating candidate models and selecting champion", db)
            self._append_log(job_id, "Computing comprehensive evaluation metrics...", db)

            best_name, best_obj, best_eval = trainer.select_best_model()
            self._append_log(job_id, f"★ Selected Champion Model: {best_name} with primary metric {best_eval['primary_metric']}", db)

            # Step 7: Packaging Single Artifact
            self._update_status(job_id, "PACKAGING", 90, "Packaging complete inference pipeline into single .aiforge file", db)
            self._append_log(job_id, "Packaging model weights, preprocessing transformers, schemas and manifest into single .aiforge file...", db)

            packaged_artifact_path = trainer.package_model(output_dir=settings.MODELS_DIR)
            self._append_log(job_id, f"Artifact created: {packaged_artifact_path.name} ({os.path.getsize(packaged_artifact_path):,} bytes)", db)

            total_duration = round(time.time() - start_time, 2)

            # Create Model Card & Record Artifact in DB
            artifact_id = str(uuid.uuid4())
            primary_metric_name = "f1_macro" if "CLASSIFICATION" in detected_task else "rmse"
            primary_metric_val = best_eval.get(primary_metric_name, best_eval.get("primary_metric", 0.0))

            model_card = {
                "model_name": packaged_artifact_path.stem,
                "task": detected_task,
                "modality": detected_modality,
                "training_dataset_samples": prep_stats.get("total_samples", prep_stats.get("train_samples", 0)),
                "best_architecture": best_name,
                "metrics": best_eval,
                "training_duration_seconds": total_duration,
                "artifact_size_bytes": os.path.getsize(packaged_artifact_path),
                "created_at": datetime.utcnow().isoformat()
            }

            model_art = ModelArtifact(
                id=artifact_id,
                job_id=job_id,
                name=packaged_artifact_path.stem,
                task=detected_task,
                modality=detected_modality,
                model_type=best_name,
                best_metric_name=primary_metric_name,
                best_metric_value=float(primary_metric_val),
                metrics_json=evaluations,
                file_path=str(packaged_artifact_path),
                file_size=os.path.getsize(packaged_artifact_path),
                schema_json=trainer.schema or {},
                metadata_json=model_card
            )
            db.add(model_art)
            db.commit()

            # Format model comparisons list
            comparisons = []
            for m_name, m_metrics in evaluations.items():
                comparisons.append({
                    "model_name": m_name,
                    "is_best": m_name == best_name,
                    **m_metrics
                })

            result_data = {
                "job_id": job_id,
                "status": "COMPLETED",
                "dataset_summary": prep_stats,
                "data_processing_summary": trainer.data_processing_summary,
                "model_comparisons": comparisons,
                "best_model_name": best_name,
                "best_metric_name": primary_metric_name,
                "best_metric_value": primary_metric_val,
                "model_artifact": {
                    "id": artifact_id,
                    "job_id": job_id,
                    "name": packaged_artifact_path.stem,
                    "task": detected_task,
                    "modality": detected_modality,
                    "model_type": best_name,
                    "best_metric_name": primary_metric_name,
                    "best_metric_value": primary_metric_val,
                    "file_size": os.path.getsize(packaged_artifact_path),
                    "created_at": datetime.utcnow(),
                    "download_url": f"/api/models/{artifact_id}/download"
                },
                "model_card": model_card,
                "confusion_matrix": best_eval.get("confusion_matrix"),
                "training_time_seconds": total_duration,
                "logs": "\n".join(self.active_jobs[job_id]["logs"])
            }

            self.active_jobs[job_id]["result"] = result_data
            self._update_status(job_id, "COMPLETED", 100, "Model successfully built and ready for download!", db)
            self._append_log(job_id, f"AutoML pipeline successfully completed in {total_duration}s. Model ready!", db)

        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}", exc_info=True)
            err_msg = str(e)
            if job_id in self.active_jobs:
                self.active_jobs[job_id]["status"] = "FAILED"
                self.active_jobs[job_id]["error"] = err_msg
            
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            if job:
                job.status = "FAILED"
                job.error_message = err_msg
                db.commit()
            self._append_log(job_id, f"ERROR: {err_msg}", db)

        finally:
            db.close()

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        if job_id in self.active_jobs:
            job_mem = self.active_jobs[job_id]
            # Check if artifact exists
            db = SessionLocal()
            try:
                art = db.query(ModelArtifact).filter(ModelArtifact.job_id == job_id).first()
                return {
                    "job_id": job_id,
                    "status": job_mem["status"],
                    "progress": job_mem["progress"],
                    "current_step": job_mem["current_step"],
                    "error_message": job_mem.get("error"),
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "has_artifact": art is not None,
                    "model_id": art.id if art else None
                }
            finally:
                db.close()

        # Database lookup
        db = SessionLocal()
        try:
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            if not job:
                return None
            art = db.query(ModelArtifact).filter(ModelArtifact.job_id == job_id).first()
            return {
                "job_id": job.id,
                "status": job.status,
                "progress": job.progress,
                "current_step": job.current_step,
                "error_message": job.error_message,
                "created_at": job.created_at,
                "updated_at": job.updated_at,
                "has_artifact": art is not None,
                "model_id": art.id if art else None
            }
        finally:
            db.close()

    def get_job_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        if job_id in self.active_jobs and self.active_jobs[job_id].get("result"):
            return self.active_jobs[job_id]["result"]

        # Restore from database
        db = SessionLocal()
        try:
            job = db.query(TrainingJob).filter(TrainingJob.id == job_id).first()
            if not job:
                return None
            art = db.query(ModelArtifact).filter(ModelArtifact.job_id == job_id).first()
            if not art:
                return None

            best_eval = art.metrics_json.get(art.model_type, {})
            comparisons = [
                {"model_name": k, "is_best": k == art.model_type, **v}
                for k, v in art.metrics_json.items()
            ]

            return {
                "job_id": job.id,
                "status": job.status,
                "dataset_summary": {},
                "data_processing_summary": ["Data cleaned, preprocessed, and validated."],
                "model_comparisons": comparisons,
                "best_model_name": art.model_type,
                "best_metric_name": art.best_metric_name,
                "best_metric_value": art.best_metric_value,
                "model_artifact": {
                    "id": art.id,
                    "job_id": job.id,
                    "name": art.name,
                    "task": art.task,
                    "modality": art.modality,
                    "model_type": art.model_type,
                    "best_metric_name": art.best_metric_name,
                    "best_metric_value": art.best_metric_value,
                    "file_size": art.file_size,
                    "created_at": art.created_at,
                    "download_url": f"/api/models/{art.id}/download"
                },
                "model_card": art.metadata_json,
                "confusion_matrix": best_eval.get("confusion_matrix"),
                "training_time_seconds": art.metadata_json.get("training_duration_seconds", 0.0),
                "logs": job.logs or ""
            }
        finally:
            db.close()
