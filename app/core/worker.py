from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time
import random
from uuid import UUID

from app.schemas.job import JobState
from app.core.logger import logger
from app.core.config import JOB_FAILURE_PROBABILITY,JOB_TIMEOUT_SECONDS
from app.repository.job_repo import JobRepository

executor = ThreadPoolExecutor(max_workers=4)

def execute_job(job_id:UUID,repo:JobRepository):
    job = repo.get_by_id(job_id)
    if not job or job.state != JobState.PENDING:
        return
    job.state = JobState.RUNNING
    job.started_at = datetime.utcnow()
    logger.info(f"Job {job_id} started")

    try:
        execution_time=random.randint(1,6)
        if execution_time>JOB_TIMEOUT_SECONDS:
            raise TimeoutError("Job timed out")
        time.sleep(execution_time)
        if random.random()<JOB_FAILURE_PROBABILITY:
            raise RuntimeError("Job failed")
        job.state=JobState.COMPLETED
        job.finished_at=datetime.utcnow()
        logger.info(f"Job {job_id} completed successfully")
    
    except Exception as e:
        job.state=JobState.FAILED
        job.finished_at=datetime.utcnow()
        logger.error(f"Job {job_id} failed: {str(e)}")