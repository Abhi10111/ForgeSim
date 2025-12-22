from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time
import random
from uuid import UUID

from app.schemas.job import JobState

executor = ThreadPoolExecutor(max_workers=4)

def execute_job(job_id:UUID,repo:JobRepository):
    job = repo.get_by_id(job_id)
    if not job or job.state != JobState.PENDING:
        return
    job.state = JobState.RUNNING
    job.started_at = datetime.utcnow()

    try:
        time.sleep(random.randint(2,5))
        job.state=JobState.COMPLETED
        job.finished_at=datetime.utcnow()
    
    except Exception:
        job.state=JobState.FAILED
        job.finished_at=datetime.utcnow()