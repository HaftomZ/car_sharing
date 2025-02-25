from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TripBase(BaseModel):
    departure_location: str
    destination_location: str
    departure_time: datetime
    available_adult_seats: int
    available_children_seats: int
    
class Booking(BaseModel):
    booker_id: int
    class Config:
        orm_mode =True

class TripDisplay(BaseModel): 
    id: int 
    car_id: int
    departure_location: str
    destination_location: str
    departure_time: datetime
    arrival_time: datetime | None = None
    available_adult_seats: int
    available_children_seats: int
    passengers_count: int | None = None
    status: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
   # trip_booked  : Booking
    class Config:
        orm_mode =True
    