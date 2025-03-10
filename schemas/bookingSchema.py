from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models.Trips import DbTrip

class Trip_Details_In_Booking(BaseModel):
   id : int
   departure_location: str
   destination_location:str
   departure_time: datetime
   class Config:
        orm_mode = True
class BookingBase(BaseModel):
    pickup_location: str
    end_location: str
    adult_seats: int
    children_seats: Optional[int]


    class Config:
        orm_mode = True
class listBookingResponse(BaseModel):
    booker_id:int
    booking_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    pickup_location: str
    end_location: str
    trip_id: int
    
     
    class Config:
        orm_mode = True
class BookingDisplay(BaseModel):
    """Schema for the response data after booking has been created or updated."""
    booking_id: int
    status: str  
    created_at: datetime
    updated_at: datetime
    adult_seats: int
    children_seats: Optional[int]
    trip: Trip_Details_In_Booking 
    class Config:
        orm_mode = True

