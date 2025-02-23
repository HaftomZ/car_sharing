from config.db_connect import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from models.Users import DbUser


class DbCar(Base):
    __tablename__ ='cars'
    id = Column(Integer,primary_key=True, index= True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    id = Column(Integer,primary_key=True, index=True)
    #owner_id = Column(Integer, ForeignKey('users.id'))
    model = Column(String)
    year = Column(Integer)
    adult_seats = Column(Integer)
    childern_seats = Column(Integer)
    smoking_allowed = Column(Boolean)
    wifi_available = Column(Boolean)
    air_conditioning = Column(Boolean)
    pet_friendly = Column(Boolean)
    car_status = Column(String, default="Pending") # Pending , approved , rejected by admin
    car_availability_status = Column(String , nullable=True)  # available , booked , in use , unavailable
    user = relationship("DbUser", back_populates='cars')
    trip_booked = relationship("DbBooking", back_populates='car')
