from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class ARNotificationLog(Base):
    __tablename__ = "ar_notification_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("ar_users.id"))
    message = Column(String)
    sent_at = Column(String)  # Store as string or use DateTime if preferred
