from sqlalchemy import Column, Integer, String, ForeignKey, func
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
    booker_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE")) # passenger and driver
    trip_id = Column(Integer, ForeignKey('trips.id', ondelete="CASCADE"))
    status = Column(String, default="pending")  # e.g., pending, confirmed, canceled    
    adult_seats = Column(Integer,  nullable=True)  
    children_seats = Column(Integer, default=0, nullable=True)
    created_at = Column(String, default=func.now())
    updated_at = Column(String, default=func.now(), onupdate=func.now())  #  auto-updated?
    pickup_location = Column(String, nullable=True)
    end_location = Column(String, nullable=True)
    #luggage = Column(String,default="no" nullable=True)  # luggage
    user = relationship("DbUser", back_populates="trip_booked")
    trip = relationship("DbTrip", back_populates="trip_booked")
