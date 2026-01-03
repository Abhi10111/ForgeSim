from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time
import random
from uuid import UUID

from app.schemas.job import Job,JobState
from app.worker.logger import logger
from app.worker.config import JOB_FAILURE_PROBABILITY,JOB_TIMEOUT_SECONDS
from app.repository.job_repo import JobRepository
from app.worker.handlers.career_handler import fetch_opportunities


executor = ThreadPoolExecutor(max_workers=4)
JOB_HANDLERS ={
    "FETCH_OPPORTUNITIES":fetch_opportunities
}

def execute_job(job:Job,repo:JobRepository):
    job.state = JobState.RUNNING
    job.started_at = datetime.utcnow()
    repo.update(job)
    logger.info(f"Job {job.id} started")

    try:
        handler=JOB_HANDLERS[job.type]
        handler()
        job.state=JobState.COMPLETED
        job.finished_at=datetime.utcnow()
        logger.info(f"Job {job.id} completed successfully")
    
    except Exception as e:
        job.state=JobState.FAILED
        job.finished_at=datetime.utcnow()
        logger.error(f"Job {job.id} failed: {str(e)}")

    repo.update(job)