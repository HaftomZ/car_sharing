from config.db_connect import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer , String , Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class DbCar(Base):
    __tablename__ ='cars'
    id = Column(Integer,primary_key=True, index= True)
    #owner_id = Column(Integer, ForeignKey('users.id'))
    model = Column(String)
    year = Column(Integer)
    adult_seats = Column(Integer)
    childern_seats = Column(Integer)
    smoking_allowed = Column(Boolean)
    wifi_available = Column(Boolean)
    air_conditioning = Column(Boolean)
    pet_friendly = Column(Boolean)
    #user = relationship("DbUser", back_populates='cars')
