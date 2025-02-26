from pydantic import BaseModel
from typing import List
from datetime import datetime

class Booking(BaseModel):
    booking_id: int
    status : str
    class Config():
        orm_mode = True
# Review inside userDisplay
class Review(BaseModel):
    mark: int
    text_description: str
    class Config():
        orm_mode = True

class Trip(BaseModel):
    departure_location: str  
    destination_location: str
    departure_time : datetime
    arrival_time: datetime | None = None
    available_adult_seats: int
    available_children_seats: int
    cost: float
    passengers_count : int | None = None
    status : str
    class Config():
        orm_mode = True

class Car(BaseModel):
    model : str
    year : int
    adult_seats : int
    children_seats : int
    smoking_allowed : bool
    wifi_available : bool
    air_conditioning : bool
    pet_friendly : bool
    car_availability_status: str | None = None
    class Config():
        orm_mode = True

class UserBase(BaseModel): 
    username: str
    email: str
    password: str
    about: str
    phone_number: str
    avatar: str


class userDisplay(BaseModel):
    user_name: str
    email: str
    about: str | None = None
    avatar: str | None = None
    phone_number: str | None = None
    left_reviews: List[Review] = []
    cars: List[Car] = []
    trip: List[Trip] = []
    trip_booked: List[Booking] = []

    class Config():
        orm_mode = True
