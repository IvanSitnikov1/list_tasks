from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict


class STaskAdd(BaseModel):
   name: str
   description: Optional[str] = None
   status: Literal['in_progress', 'completed']


class STask(STaskAdd):
   id: int
   model_config = ConfigDict(from_attributes=True)


class STaskId(BaseModel):
   id: int
