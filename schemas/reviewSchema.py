from pydantic import BaseModel
from enum import Enum


class UserRating(int, Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5



# User inside ReviewDisplay
class User(BaseModel):
    id: int
    user_name: str
    class Config():
        orm_mode = True


class ReviewBase(BaseModel):
    rating: UserRating
    creator_id: int
    receiver_id: int
    text_description: str | None = None


class ReviewDisplay(BaseModel):
    id: int
    rating: int
    text_description: str
    creator_id: int
    receiver_id: int
    photos: str | None = ""
    class Config():
        orm_mode = True
