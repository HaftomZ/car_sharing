from config.db_connect import Base
from sqlalchemy import Column, Integer, String, Enum
from enum import Enum as PyEnum

class AdminRole(PyEnum):
    super_admin = "superAdmin"
    moderator = "moderator"

class DbAdmin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(AdminRole), nullable=False)
