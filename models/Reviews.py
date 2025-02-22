from database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer

class DbReview (Base):
    __tablename__ = 'reviews'

