from sqlalchemy import Column, Integer, String
from app.database import Base

class ARHall(Base):
    __tablename__ = "ar_halls"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    capacity = Column(Integer)
    status = Column(String)  # Available / Booked
