from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.db_connect import Base

import datetime
# class BookingStatus(str,Enum):
#     pending = "pending" 
#     confirmed = "confirmed"
#     canceled = "canceled"

class DbBooking(Base):
    __tablename__ = "bookings"


    booking_id = Column(Integer, primary_key=True, index=True)
    booker_id = Column(Integer, ForeignKey('users.id')) # passenger and driver
    ride_id = Column(Integer, ForeignKey('trips.id')) 
    status = Column(String, default="pending")  # e.g., pending, confirmed, canceled    
    adult_seats = Column(Integer,  nullable=True)  # number of seats  
    children_seats = Column(Integer, default= 0, nullable=True)  # number of seats
    created_at = Column(DateTime, default=datetime.datetime.now)  # Created at timestamp
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # Updated at timestamp, auto-updated
    pickup_location = Column(String, nullable=True)  # pick up Location 
    #luggage = Column(String,default="no" nullable=True)  # luggage
    user = relationship("DbUser", back_populates="trip_booked")
    trip = relationship("DbTrip", back_populates="trip_booked")
