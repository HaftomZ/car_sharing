from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from config.db_connect import Base
from datetime import timezone,datetime

class DbBooking(Base):
    __tablename__ = "bookings"


    booking_id = Column(Integer, primary_key=True, index=True)
    booker_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE")) # passenger and driver
    trip_id = Column(Integer, ForeignKey('trips.id', ondelete="CASCADE"))
    status = Column(String, default="Pending")  # e.g., pending, confirmed    
    adult_seats = Column(Integer,  nullable=True)  
    children_seats = Column(Integer, default= 0, nullable=True)  
    created_at =Column(DateTime, default=datetime.now(timezone.utc))  
    updated_at = Column(String, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))  
    pickup_location = Column(String, nullable=True)
    end_location = Column(String, nullable=True)
    #luggage = Column(String,default="no" nullable=True)  # luggage
    user = relationship("DbUser", back_populates="trip_booked")
    trip = relationship("DbTrip", back_populates="trip_booked")
    payment = relationship("DbPayment", back_populates="trip_booked")
