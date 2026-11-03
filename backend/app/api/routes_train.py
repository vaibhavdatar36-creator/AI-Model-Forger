from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.jobs.manager import JobManager
from app.schemas.requests import TrainRequest
from app.schemas.responses import JobStatusResponse, JobResultResponse

router = APIRouter(prefix="/api", tags=["train"])
job_manager = JobManager()

@router.post("/train", response_model=JobStatusResponse)
async def start_training(
    request: TrainRequest,
    db: Session = Depends(get_db)
):
    options = {}
    if request.advanced_settings:
        options = request.advanced_settings.dict(exclude_none=True)
    if request.selected_model:
        options["model_choice"] = request.selected_model

    job_id = job_manager.start_training_job(
        dataset_id=request.dataset_id,
        requirement=request.requirement,
        project_name=request.project_name or "AI Model Forge Project",
        options=options
    )

    status_data = job_manager.get_job_status(job_id)
    return JobStatusResponse(**status_data)

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    status_data = job_manager.get_job_status(job_id)
    if not status_data:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    return JobStatusResponse(**status_data)

@router.get("/results/{job_id}", response_model=JobResultResponse)
async def get_job_results(job_id: str):
    result_data = job_manager.get_job_result(job_id)
    if not result_data:
        raise HTTPException(status_code=404, detail=f"Results for job {job_id} not found or job still running.")
    return JobResultResponse(**result_data)
