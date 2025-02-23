from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class TripBase(BaseModel):
    """Base schema for trip data shared by both creating and updating trips."""
    triper_id: int
    car_id: int
    available_seats: int
    status: str
    departure_location: str
    destination_location: str
    departure_time: datetime
    class Config:
        orm_mode =True
class TripResponse(BaseModel):
    """Schema for the response data after trip has been created or updated."""  
    status: str
    created_at: datetime
    updated_at: datetime
    departure_time: datetime
    message: str
    class Config:
        orm_mode =True
    