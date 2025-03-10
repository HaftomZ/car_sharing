from pydantic import BaseModel , Field
from typing import Optional


class User(BaseModel):
    id: int
    user_name: str
    class Config():
        orm_mode = True


class ReportBase(BaseModel):
    creator_id : int
    reported_id : int
    reason : str = Field(..., min_length=5, max_length=100, description="Reason for the report")
    details : Optional[str] = Field(None, max_length=500, description="Additional details about the report")


class ReportDisplay(BaseModel):
    id: int
    creator_id : int
    reported_id : int
    reason : str
    details : Optional[str] 
    status: str
    created_at : str
    class Config():
        orm_mode = True
