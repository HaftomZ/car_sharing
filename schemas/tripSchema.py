from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from typing import List

class TripBase(BaseModel):
    departure_location: str
    destination_location: str
    departure_time: datetime
    arrival_time: datetime
    available_adult_seats: int
    available_children_seats: int
    cost: float

class Booking(BaseModel):
    booker_id: int 
    status: str
    adult_seats: int
    children_seats: int 
    pickup_location: str
    class Config:
        orm_mode =True

class TripDisplay(BaseModel): 
    id: int 
    car_id: int
    departure_location: str
    destination_location: str
    departure_time: datetime
    arrival_time: datetime | None = None
    duration: float
    available_adult_seats: int
    available_children_seats: int
    cost: float
    passengers_count: int | None = None
    status: str | None = None
    created_at: str
    updated_at: str | None = None
    trip_booked: List[Booking] = []
   # trip_booked  : Booking
    class Config:
        orm_mode =True
    