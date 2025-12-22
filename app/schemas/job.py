from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4

class JobCreate(BaseModel):
    title:str
    company:str
    location:str
    description:Optional[str]=None

class Job(JobCreate):
    id:UUID

