from pydantic import BaseModel


#User inside ReviewDisplay
class User(BaseModel):
    id: int
    username: str
    class Config():
        orm_mode = True

class ReviewBase(BaseModel):
    mark = int
    text_description = str
    creator_id: int


class ReviewDisplay(BaseModel):
    mark = int
    text_description = str
    user: User

    class Config():
        orm_mode = True
