from pydantic import BaseModel
from datetime import date

class RoleCreate(BaseModel):
    name: str

class UserCreate(BaseModel):
    name: str
    email: str
    role_id: int

class ProjectCreate(BaseModel):
    name: str
    description: str

class TaskCreate(BaseModel):
    title:str
    description: str
    status: str
    due_date: date
    project_id: int
    owner_id: int
