from pydantic import BaseModel , Field
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
    status: str #= Field(..., description ="scheduled, ongoing, completed, or cancelled")
    cost: float
    creator_id: int
    car_id : int


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
    departure_location: str
    destination_location: str
    departure_time: datetime
    arrival_time: datetime
    duration: float
    available_adult_seats: int
    available_children_seats: int
    cost: float
    passengers_count: int | None = None
    status: str | None = None
    created_at: str
    updated_at: str | None = None
    car_id: int
    creator_id: int
    trip_booked: List[Booking] = []
   # trip_booked  : Booking
    class Config:
        orm_mode =True
    