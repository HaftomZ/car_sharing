from config.db_connect import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
# from models.Cars import DbCar
# from models.Reviews import DbReview
# from models.Booking import DbBooking


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    user_name = Column(String)
    email = Column(String)
    password = Column(String)
    about = Column(String)
    avatar = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    car = relationship("DbCar", back_populates="users")
    trip_booked = relationship("DbBooking", back_populates='users')
    