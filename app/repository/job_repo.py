import os
import json
from threading import Lock
from typing import List, Optional
from uuid import UUID

from app.schemas.job import Job

class JobRepository:
    def __init__(self,path="/data/jobs.json"):
        self.path = path
        self._lock = Lock()

        if not os.path.exists(self.path):
            with open(self.path,"w") as f:
                json.dump([],f)

    def _read(self)->List[dict]:
        with open(self.path,"r") as f:
            return json.load(f)

    def _write(self,data:List[dict]):
        with open(self.path,"w") as f:
            json.dump(data,f)

    def add(self, job: Job):
        with self._lock:
            jobs=self._read()
            jobs.append(job.model_dump(mode='json'))
            self._write(jobs)

    def get_all(self) -> List[Job]:
        with self._lock:
            return [Job(**j) for j in self._read()]

    def get_by_id(self, job_id: UUID) -> Optional[Job]:
        with self._lock:
            for j in self._read():
                if j["id"] == str(job_id):
                    return Job(**j)
        return None

    def update(self, updated_job: Job):
        with self._lock:
            jobs = self._read()
            for i in range(len(jobs)):
                if jobs[i]["id"] == str(updated_job.id):
                    jobs[i] = updated_job.model_dump(mode='json')
                    break
            self._write(jobs)
