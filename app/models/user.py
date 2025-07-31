from sqlalchemy import Column, Integer, String
from app.database import Base

class ARUser(Base):
    __tablename__ = "ar_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    role = Column(String)  # 'admin' or 'user'
