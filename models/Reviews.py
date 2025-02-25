from config.db_connect import Base
from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import ForeignKey
from models.Users import DbUser
from sqlalchemy.orm import relationship


class DbReview (Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    creator_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(String, default=func.now())
    mark = Column(Integer)
    text_description = Column(String)
    creator = relationship("DbUser", foreign_keys=[creator_id], back_populates="left_reviews")







