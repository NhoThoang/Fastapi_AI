from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.base import Base
from sqlalchemy import CheckConstraint
from datetime import datetime
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_product = Column(String(255), nullable=False)
    barcode = Column(String(20), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    import_price = Column(Integer, nullable=False)
    sell_price = Column(Integer, nullable=False)
    discount = Column(Integer, CheckConstraint('discount >= 0 AND discount <= 100'), nullable=False, default=0)
    input_date = Column(DateTime, nullable=False, default=datetime.now)
    expiry_date = Column(DateTime, nullable=False)
    type_product = Column(String(50, collation='utf8mb4_bin'), index=True)