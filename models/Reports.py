from config.db_connect import Base
from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class DbReport (Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    reported_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    reason = Column(String)
    details = Column(String, nullable=True)
    status = Column(String,default="pending") #pending, resolved, rejected
    created_at = Column(String, default=func.now())
    creator = relationship("DbUser", back_populates="created_reports", foreign_keys=[creator_id])
    reported = relationship("DbUser", back_populates="received_reports", foreign_keys=[reported_id])








