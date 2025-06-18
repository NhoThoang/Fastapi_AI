from sqlalchemy import Column, Integer, String, Boolean
from app.db.mysql.base import Base

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50, collation='utf8mb4_bin'), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(100), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    admin = Column(Boolean, nullable=False, default=False)
    count_refresh_token = Column(Integer, nullable=False, default=0)
    refresh_token = Column(String(225))
    def __repr__(self):
        return f"<account(id={self.id}, username={self.username}, active={self.active})>"