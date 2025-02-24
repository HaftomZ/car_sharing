from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TripBase(BaseModel):
    departure_location: str
    destination_location: str
    departure_time: datetime
    available_adult_seats: int
    available_children_seats: int
    

class TripDisplay(BaseModel):  
    departure_location: str
    destination_location: str
    departure_time: datetime
    available_adult_seats: int
    available_children_seats: int
    class Config:
        orm_mode =True
    