from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class JobCreate(BaseModel):
    title:str
    company:str
    location:str
    description:Optional[str]=None

class JobState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    
class Job(JobCreate):
    id:UUID
    state:JobState
    created_at:datetime
    started_at:Optional[datetime]=None
    finished_at:Optional[datetime]=None


