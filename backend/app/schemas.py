from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class TaskCreate(BaseModel):
    title: str
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[str] = None
    project_id: int
    status: str = "pending"

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be blank")
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")
    due_date: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    due_date: Optional[str]
    status: str
    project_id: int

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    name: str
    owner_id: int

class ProjectResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True