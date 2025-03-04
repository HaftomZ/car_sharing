from pydantic import BaseModel


# User inside ReviewDisplay
class User(BaseModel):
    id: int
    user_name: str
    class Config():
        orm_mode = True


class ReviewBase(BaseModel):
    #rating: int
    text_description: str | None = None
    #creator_id: int
    #receiver_id: int


class ReviewDisplay(BaseModel):
    rating: int
    text_description: str
    creator_id: int
    receiver_id: int
    class Config():
        orm_mode = True
