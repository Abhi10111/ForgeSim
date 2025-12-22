from fastapi import APIRouter
from typing import List
from uuid import uuid4

from app.schemas.job import Job,JobCreate

router=APIRouter(prefix='/jobs',tags=["Jobs"])

JOBS_DB=[]

@router.post("/",response_model=Job)
def create_job(job:JobCreate):
    new_job=Job(id=uuid4(),**job.dict())
    JOBS_DB.append(new_job)
    return new_job

@router.get("/",response_model=List[Job])
def list_jobs():
    return JOBS_DB
