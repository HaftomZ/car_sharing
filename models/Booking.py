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


    id = Column(Integer, primary_key=True, index=True)
    #user_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to users table
    #car_id = Column(Integer, ForeignKey("cars.id"))  # Foreign key to cars table
    start_time = Column(DateTime, default=datetime.datetime.now())
    end_time = Column(DateTime)
    status = Column(String, default="pending")  # e.g., pending, confirmed, canceled    
    booking_id = Column(Integer, primary_key=True, index=True)
    booker_id = Column(Integer, ForeignKey('users.id')) # passenger and driver
    ride_id = Column(Integer, ForeignKey('trips.id')) 
    start_time = Column(DateTime, default=datetime.datetime.now)  
    status = Column(String, default="pending")  # e.g., pending, confirmed, canceled
    created_at = Column(DateTime, default=datetime.datetime.now)  # Created at timestamp
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # Updated at timestamp, auto-updated
    pickup_location= Column(String, nullable=True)  # pick up Location 
    user = relationship("DbUser", back_populates="trip_booked")
    trip = relationship("DbTrip", back_populates="trip_booked")
