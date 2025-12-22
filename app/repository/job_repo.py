from threading import Lock
from typing import List, Optional
from uuid import UUID

from app.schemas.job import Job

class JobRepository:
    def __init__(self):
        self._jobs: List[Job] = []
        self._lock = Lock()

    def add(self, job: Job):
        with self._lock:
            self._jobs.append(job)

    def get_all(self) -> List[Job]:
        with self._lock:
            return list(self._jobs)

    def get_by_id(self, job_id: UUID) -> Optional[Job]:
        with self._lock:
            return next((j for j in self._jobs if j.id == job_id), None)

    def update(self, job: Job):
        # Objects are mutated in place, lock protects visibility
        pass
