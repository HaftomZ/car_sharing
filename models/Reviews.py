from config.db_connect import Base
from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class DbReview (Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    receiver_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    creator_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    created_at = Column(String, default=func.now())
    rating = Column(Integer)
    text_description = Column(String, nullable=True)
    photos = Column(String, nullable=True)
    creator = relationship("DbUser", back_populates="left_reviews", foreign_keys=[creator_id])
    receiver = relationship("DbUser", back_populates="received_reviews", foreign_keys=[receiver_id])








