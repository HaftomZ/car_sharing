from pydantic import BaseModel, EmailStr

class AdminBase(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminDisplay(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True
