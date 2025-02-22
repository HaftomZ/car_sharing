from pydantic import BaseModel


class ReviewBase(BaseModel):
    mark = int
    text_description = str


class ReviewDisplay(BaseModel):
    mark = int
    text_description = str

    class Config():
        orm_mode = True
