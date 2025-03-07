from sqlalchemy import Column, Integer, String, ForeignKey, Float,DateTime,Boolean
from sqlalchemy.orm import relationship
from config.db_connect import Base
from datetime import datetime,timezone

class DbPayment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, default="Euro")
    status = Column(String, default="Pending")
    payment_method = Column(String,default="Credit card")
    transaction_reference = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    refund_status = Column(Boolean, default=False)
    admin_approved = Column(Boolean, default=False)
    

    trip_booked = relationship("DbBooking", back_populates="payment")
    user = relationship("DbUser", back_populates="payment")
