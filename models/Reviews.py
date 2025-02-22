from config.db_connect import Base
from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String


class DbReview (Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    username = Column()
    author = Column()
    created_at = Column(String, default=func.now())
    mark = Column(Integer)
    text = Column(String)







