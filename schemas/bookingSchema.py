from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models.Trips import DbTrip

class Trip_Details_In_Booking(BaseModel):
   
   departure_location: str
   destination_location:str
   #departure_time: datetime
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
    booking_id: int
    trip_id: int
    status: str
    created_at: str
    updated_at: str
    pickup_location: str
    trip: Trip_Details_In_Booking 
    end_location: str
    
     
    class Config:
        orm_mode = True
class BookingDisplay(BaseModel):
    """Schema for the response data after booking has been created or updated."""

    status: str  
    created_at: str
    updated_at: str
    #message:str
    trip: Trip_Details_In_Booking 
    class Config:
        orm_mode = True

