from fastapi import APIRouter,HTTPException
from typing import List
from uuid import uuid4
from datetime import datetime
from threading import Lock
from uuid import UUID

from app.schemas.job import Job,JobCreate,JobState
from app.repository.job_repo import JobRepository

jobs_lock=Lock()

router=APIRouter(prefix='/jobs',tags=["Jobs"])

repo = JobRepository()


@router.post("/",response_model=Job)
def create_job(job:JobCreate):
    new_job=Job(id=uuid4(),state=JobState.PENDING,created_at=datetime.utcnow(),**job.dict())
    repo.add(new_job)
    return new_job

@router.post("/{job_id}/run")
def run_job(job_id: UUID):
    job = repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.state != JobState.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Only PENDING jobs can be executed"
        )

    job.state=JobState.QUEUED
    repo.update(job)
    return {"message": "Job queued"}

@router.get("/",response_model=List[Job])
def list_jobs():
    return repo.get_all()