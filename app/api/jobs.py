from fastapi import APIRouter,HTTPException
from typing import List
from uuid import uuid4
from datetime import datetime
from app.schemas.job import Job,JobCreate,JobState

router=APIRouter(prefix='/jobs',tags=["Jobs"])

JOBS_DB:List[Job]=[]

@router.post("/",response_model=Job)
def create_job(job:JobCreate):
    new_job=Job(id=uuid4(),state=JobState.PENDING,created_at=datetime.utcnow(),**job.dict())
    JOBS_DB.append(new_job)
    return new_job

@router.post("/{job_id}/start",response_model=Job)
def start_job(job_id:str):
    for job in JOBS_DB:
        if str(job.id) == job_id:
            if job.state != JobState.PENDING:
                raise HTTPException(status_code=400,detail="Only PENDING jobs can be started")
            job.state=JobState.RUNNING
            job.started_at=datetime.utcnow()
            return job
    raise HTTPException(status_code=404,detail="Job not found")

@router.post("/{job_id}/complete",response_model=Job)
def complete_job(job_id:str):
    for job in JOBS_DB:
        if str(job.id) == job_id:
            if job.state != JobState.RUNNING:
                raise HTTPException(status_code=400,detail="Only RUNNING jobs can be completed")
            job.state=JobState.COMPLETED
            job.finished_at=datetime.utcnow()
            return job
    raise HTTPException(status_code=404,detail="Job not found")

@router.post("/{job_id}/fail",response_model=Job)
def complete_job(job_id:str):
    for job in JOBS_DB:
        if str(job.id)== job_id:
            if job.state != JobState.RUNNING:
                raise HTTPException(status_code=400,detail="Only RUNNING jobs can fail")
            job.state=JobState.FAILED
            job.finished_at=datetime.utcnow()
            return job
    raise HTTPException(status_code=404,detail="Job not found")

@router.get("/",response_model=List[Job])
def list_jobs():
    return JOBS_DB
