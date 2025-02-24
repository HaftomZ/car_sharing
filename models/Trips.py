from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from enum import Enum
from sqlalchemy.orm import relationship
from config.db_connect import Base
import datetime
class DbTrip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    triper_id = Column(Integer, ForeignKey('users.id'))  # driver only
    car_id = Column(Integer, ForeignKey('cars.id'))  
    departure_location= Column(String, nullable=True)  
    destination_location= Column(String, nullable=True)
    departure_time = Column(DateTime, default=datetime.datetime.now)  # start time
    arrival_time = Column(DateTime, nullable=True)  # end time
    available_adult_seats = Column(Integer, nullable=True)  # available seats
    available_children_seats = Column(Integer, nullable=True)  # available seats
    passengers = Column(String, default="Haftom", nullable=True)  # This should be changed later in to list of passengers
    status = Column(String, default="open", nullable=True)  # e.g. open, closed, canceled
    created_at = Column(DateTime, default=datetime.datetime.now)  # Created at timestamp
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # Updated at timestamp, auto-updated
    user = relationship("DbUser", back_populates="trip")
    car = relationship("DbCar", back_populates="trip")
    trip_booked = relationship("DbBooking", back_populates="trip")