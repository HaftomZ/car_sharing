from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config.db_connect import Base
import datetime

class DbBooking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.datetime.now)  # Use utcnow for consistency
    end_time = Column(DateTime)
    status = Column(String, default="pending")  # e.g., pending, confirmed, canceled
    created_at = Column(DateTime, default=datetime.datetime.now)  # Created at timestamp
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # Updated at timestamp, auto-updated
    location = Column(String, nullable=True)  # Location of the booking