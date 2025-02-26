from pydantic import BaseModel, EmailStr, field_validator
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
    cars: List[Car] = []
    trip_booked: List[Booking] = []

    class Config():
        orm_mode = True

    

       



