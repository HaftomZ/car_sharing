from pydantic import BaseModel
from datetime import datetime
from typing import Optional
# BookingList inside listBookingResponse
class BookingList(BaseModel):
    booking_id: int
    start_time: datetime
    end_time: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    location: str
    class Config:
        orm_mode = True
class BookingBase(BaseModel):
    """Base schema for booking data shared by both creating and updating bookings."""
    booker_id: int
    car_id: int
    start_time: datetime
    end_time: datetime
    location: str

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
    end_time: datetime
    location: str
    message:str
    class Config:
        orm_mode = True

