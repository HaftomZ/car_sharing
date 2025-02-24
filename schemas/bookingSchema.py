from pydantic import BaseModel
from datetime import datetime
from typing import Optional
# BookingList inside listBookingResponse
class BookingList(BaseModel):
    booking_id: int
    start_time: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    pickup_location: str
    class Config:
        orm_mode = True
class BookingBase(BaseModel):
    """Base schema for booking data shared by both creating and updating bookings."""
    ride_id: int
    booker_id: int
    start_time: datetime
    pickup_location: str

    class Config:
        orm_mode = True
class listBookingResponse(BaseModel):
    booking_list:list[BookingList] =[]
    class Config:
        orm_mode = True
class BookingResponse(BaseModel):
    """Schema for the response data after booking has been created or updated."""
    status: str  
    created_at: datetime
    updated_at: datetime
    start_time: datetime
    
    message:str
    class Config:
        orm_mode = True

