from config.db_connect import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
# from models.Cars import DbCar
# from models.Reviews import DbReview
# from models.Booking import DbBooking
#from models.Reports import DbReport

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    about = Column(String)
    avatar = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    cars = relationship("DbCar", back_populates="user", cascade="all, delete-orphan")
    trip_booked = relationship("DbBooking", back_populates="user", cascade="all, delete-orphan")
    average_rating = Column(Float)
    left_reviews = relationship("DbReview", back_populates="creator", foreign_keys="[DbReview.creator_id]")
    received_reviews = relationship("DbReview", back_populates="receiver", foreign_keys="[DbReview.receiver_id]",
                                    cascade="all, delete-orphan")
    trip = relationship("DbTrip", back_populates="user", cascade="all, delete-orphan")
    reviews_received_count = Column(Integer, nullable=True)
    payment = relationship("DbPayment", back_populates="user")
    is_verified = Column(Boolean, default=False)
    created_reports = relationship("DbReport", back_populates="creator", foreign_keys="[DbReport.creator_id]")
    received_reports = relationship("DbReport", back_populates="reported", foreign_keys="[DbReport.reported_id]")



