
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)

class BookingRequest(Base):
    __tablename__ = "booking_requests"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    hall = Column(String)
    date = Column(String)
    time = Column(String)
    status = Column(String)
    user_id = Column(String)
   
