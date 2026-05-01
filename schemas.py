from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    category: str = Field(default="Дом")

class TaskOut(BaseModel):
    id: int
    title: str
    category: str
    is_completed: bool

    class Config:
        from_attributes = True
