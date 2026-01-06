import time
import datetime
import os
from app.worker.worker import executor
from app.worker.logger import logger
from app.worker.config import *
from app.repository.job_repo import JobRepository
from app.schemas.job import JobState
from app.worker.worker import executor, execute_job,slots
repo=JobRepository()

# Worker process stays alive
if __name__ == "__main__":
    print("Worker started, polling for jobs...")
    while True:
        jobs = repo.get_all()
        for job in jobs:
            if job.state==JobState.QUEUED and slots.acquire(blocking=False):
                job.state = JobState.RUNNING
                job.started_at = datetime.utcnow()
                repo.update(job)
                logger.info(f"Job {job.id} started")
                executor.submit(execute_job,job,repo)
        time.sleep(POLL_INTERVAL)