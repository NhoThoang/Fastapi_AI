from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db.base import Base
class UserDevice(Base):
    __tablename__ = 'user_device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50, collation='utf8mb4_bin'), nullable=False, index=True)
    device_id = Column(String(36, collation='utf8mb4_bin'), nullable=False, index=True)
    user_agent = Column(String(255))
    ip_address = Column(String(45))
    is_trusted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, default=datetime.now)