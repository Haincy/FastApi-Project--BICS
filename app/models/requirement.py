from sqlalchemy import Column, Integer, String
from app.database import Base

class ARBookingRequirement(Base):
    __tablename__ = "ar_booking_requirements"
    id = Column(Integer, primary_key=True, index=True)
    requirement_name = Column(String)
    description = Column(String)
