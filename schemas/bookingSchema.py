from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    """Base schema for booking data shared by both creating and updating bookings."""
    booking_id: int
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None  # Making location optional
    status: Optional[str] = None    # Making status optional
    created_at: Optional[datetime] = None  # Optional field for created_at
    updated_at: Optional[datetime] = None  # Optional field for updated_at

    class Config:
        orm_mode = True

class BookingCreate(BookingBase):
    """Schema for creating a new booking, but doesn’t add any additional fields,
    because all fields required to create a booking are already covered by BookingBase"""
    pass

class BookingUpdate(BookingBase):
    """Schema for updating an existing booking."""
    # Removed redundant booking_id here

class BookingResponse(BookingBase):
    """Schema for the response data after booking has been created or updated."""
    booking_id: Optional[int]
    status: Optional[str] = None  # status is optional
    created_at: datetime
    updated_at: datetime
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None  # location is optional

    class Config:
        orm_mode = True

