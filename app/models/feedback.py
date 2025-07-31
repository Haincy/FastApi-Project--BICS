from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class ARFeedback(Base):
    __tablename__ = "ar_feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("ar_users.id"))
    message = Column(String)
    rating = Column(Integer)  # 1 to 5
