from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from enum import Enum
from sqlalchemy.orm import relationship
from config.db_connect import Base
import datetime
class DbTrip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    car_id = Column(Integer, ForeignKey('cars.id', ondelete="CASCADE"))
    departure_location= Column(String)  
    destination_location= Column(String)
    departure_time = Column(DateTime) 
    arrival_time = Column(DateTime, nullable=True)
    available_adult_seats = Column(Integer)
    available_children_seats = Column(Integer)
    passengers_count = Column(Integer, nullable=True)
    status = Column(String, default="Scheduled", nullable=True) # scheduled, ongoing, completed, or cancelled
    created_at = Column(DateTime, default=datetime.datetime.now) 
    updated_at = Column(DateTime, nullable=True)
    user = relationship("DbUser", back_populates="trip")
    car = relationship("DbCar", back_populates="trip")
    trip_booked = relationship("DbBooking", back_populates="trip")