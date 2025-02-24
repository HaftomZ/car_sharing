from pydantic import BaseModel


# User inside ReviewDisplay
class User(BaseModel):
    id: int
    user_name: str
    class Config():
        orm_mode = True


class ReviewBase(BaseModel):
    mark: int
    text_description: str
    creator_id: int
    user_id: int


class ReviewDisplay(BaseModel):
    mark: int
    text_description: str
    user_id: int
    creator_id: int


    class Config():
        orm_mode = True
