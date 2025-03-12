from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models.Trips import DbTrip
class BookingBase(BaseModel):
    booker_id : int
    trip_id: int
    pickup_location: str
    end_location: str
    adult_seats: int
    children_seats: Optional[int]
    class Config:
        orm_mode = True
class BookingDisplay(BaseModel):
    """Schema for the response data after booking has been created or updated."""
    booking_id: int
    booker_id: int
    trip_id: int
    status: str 
    pickup_location: str
    end_location: str 
    created_at: datetime
    updated_at: datetime
    adult_seats: int
    children_seats: Optional[int]
    
    class Config:
        orm_mode = True

