from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.db.mysql.base import Base
from sqlalchemy import CheckConstraint
from datetime import datetime
from sqlalchemy import Index
from sqlalchemy.orm import relationship
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
     # Relationship tới ảnh
    images = relationship("Product_images", back_populates="product", cascade="all, delete-orphan")
class Product_images(Base):
    __tablename__ = 'product_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    barcode = Column(String(50), ForeignKey("products.barcode"), nullable=False)
    image_hash = Column(String(255), index=True, nullable=False)
    image_url = Column(String(255), nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    is_delete = Column(Boolean, nullable=False, default=False)

    # Quan hệ n-1 với bảng Products
    product = relationship("Products", back_populates="images")

    __table_args__ = (
        Index("idx_username_barcode", "username", "barcode"),
    )