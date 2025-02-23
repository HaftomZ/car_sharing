from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from enum import Enum
from sqlalchemy.orm import relationship
from config.db_connect import Base
import datetime
# class TripStatus(str,Enum):
#     open = "open"
#     closed = "closed"   
#     canceled = "canceled"
class DbTrip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    triper_id = Column(Integer, ForeignKey('users.id'))  # driver and passenger
    car_id = Column(Integer, ForeignKey('cars.id'))  
    departure_location= Column(String, nullable=True)  
    destination_location= Column(String, nullable=True)
    departure_time = Column(DateTime, default=datetime.datetime.now)  # start time
    available_seats = Column(Integer, nullable=True)  # available seats
    status = Column(String, default="open", nullable=True)  # e.g., pending, confirmed, canceled
    created_at = Column(DateTime, default=datetime.datetime.now)  # Created at timestamp
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # Updated at timestamp, auto-updated
    user = relationship("DbUser", back_populates="trip")
    car = relationship("DbCar", back_populates="trip")
    trip_booked = relationship("DbBooking", back_populates="trip")