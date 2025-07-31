from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class ARBooking(Base):
    __tablename__ = "ar_bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("ar_users.id"))
    hall_id = Column(Integer, ForeignKey("ar_halls.id"))
    date = Column(String)
    time_slot = Column(String)
    purpose = Column(String)
    status = Column(String)  # Pending / Approved / Rejected
