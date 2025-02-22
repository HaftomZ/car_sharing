from pydantic import BaseModel


class ReviewBase(BaseModel):
    mark = int
    text_description = str
