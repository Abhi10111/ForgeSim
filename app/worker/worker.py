import time
import random
from threading import Semaphore
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from uuid import UUID

from app.schemas.job import Job,JobState
from app.worker.logger import logger
from app.worker.config import MAX_WORKERS
from app.repository.job_repo import JobRepository
from app.worker.handlers.career_handler import fetch_opportunities


executor = ThreadPoolExecutor(max_workers=4)
slots = Semaphore(MAX_WORKERS)

JOB_HANDLERS ={
    "FETCH_OPPORTUNITIES":fetch_opportunities
}

def execute_job(job:Job,repo:JobRepository):
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

    finally:
        repo.update(job)
        slots.release()