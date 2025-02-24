from pydantic import BaseModel
from typing import List

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

class Car(BaseModel):
    model : str
    year : int
    adult_seats : int
    childern_seats : int
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
    cars: List[Car] = []
    lefted_reviews: List[Review] = []
    bookings: List[Booking] = []
    class Config():
        orm_mode = True
