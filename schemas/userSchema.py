from pydantic import BaseModel
from typing import List


# Review inside userDisplay
class Review(BaseModel):
    mark: int
    text_description: str
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
    class Config():
        orm_mode = True
