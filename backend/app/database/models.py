from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    requirement = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    datasets = relationship("Dataset", back_populates="project", cascade="all, delete-orphan")
    jobs = relationship("TrainingJob", back_populates="project", cascade="all, delete-orphan")

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    modality = Column(String(64), nullable=True)
    row_count = Column(Integer, nullable=True)
    col_count = Column(Integer, nullable=True)
    profile_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="datasets")
    jobs = relationship("TrainingJob", back_populates="dataset")

class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    dataset_id = Column(String(36), ForeignKey("datasets.id"), nullable=True)
    status = Column(String(32), default="UPLOADING") # UPLOADING, ANALYZING, PREPROCESSING, TRAINING, EVALUATING, PACKAGING, COMPLETED, FAILED
    progress = Column(Integer, default=0)
    current_step = Column(String(255), default="Initializing")
    logs = Column(Text, default="")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="jobs")
    dataset = relationship("Dataset", back_populates="jobs")
    artifact = relationship("ModelArtifact", back_populates="job", uselist=False, cascade="all, delete-orphan")

class ModelArtifact(Base):
    __tablename__ = "model_artifacts"

    id = Column(String(36), primary_key=True)
    job_id = Column(String(36), ForeignKey("training_jobs.id"), nullable=False)
    name = Column(String(255), nullable=False)
    task = Column(String(64), nullable=False)
    modality = Column(String(64), nullable=False)
    model_type = Column(String(128), nullable=False)
    best_metric_name = Column(String(64), nullable=False)
    best_metric_value = Column(Float, nullable=False)
    metrics_json = Column(JSON, nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    schema_json = Column(JSON, nullable=False)
    metadata_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("TrainingJob", back_populates="artifact")
