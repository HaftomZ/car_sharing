from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.db_connect import Base  
import datetime

class DbBooking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    #user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to users table
    #car_id = Column(Integer, ForeignKey("cars.id"))  # Foreign key to cars table
    start_time = Column(DateTime, default=datetime.datetime.now())
    end_time = Column(DateTime)
    status = Column(String, default="pending")  # e.g., pending, confirmed, canceled

    #user = relationship("User", back_populates="bookings")
    #car = relationship("Car", back_populates="bookings")
