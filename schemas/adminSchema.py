from pydantic import BaseModel, EmailStr
from enum import Enum as PyEnum

class AdminRole(str, PyEnum):
    super_admin = "superAdmin"
    moderator = "moderator"

class AdminBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: AdminRole

class AdminDisplay(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: AdminRole

    class Config:
        from_attributes = True
