from pydantic import BaseModel, EmailStr, field_validator
from typing import List
from datetime import datetime

class Booking(BaseModel):
    booking_id: int
    status : str
    class Config():
        orm_mode = True
# Review inside userDisplay
class Review(BaseModel):
    rating: int
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
    total_seats : int
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


    @field_validator("about")
    @classmethod
    def validate_about_length(cls, value):
        if len(value) >= 300:
            raise ValueError("About section cannot exceed 300 characters.")
        return value


class userDisplay(BaseModel):
    user_name: str
    email: EmailStr
    about: str | None = None
    avatar: str | None = None
    phone_number: str | None = None
    left_reviews: List[Review] = []
    received_reviews: List[Review] = []
    cars: List[Car] = []
    trip: List[Trip] = []
    trip_booked: List[Booking] = []

    class Config():
        orm_mode = True

    

       



