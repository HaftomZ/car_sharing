from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    """Base schema for booking data shared by both creating and updating bookings."""
    trip_id: int
    booker_id: int
    pickup_location: str
    end_location: str
    adult_seats: int
    children_seats: Optional[int]


    class Config:
        orm_mode = True
class listBookingResponse(BaseModel):
    booking_id: int
    trip_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    pickup_location: str
    end_location: str
    
     
    class Config:
        orm_mode = True
class BookingDisplay(BaseModel):
    """Schema for the response data after booking has been created or updated."""
    status: str  
    created_at: datetime
    updated_at: datetime
    message:str
    class Config:
        orm_mode = True

