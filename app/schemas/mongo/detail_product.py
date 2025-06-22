from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from .product_common import DescriptionBlock, SEO
from app.schemas.mysql.product import ProductBase

class ProductDetailIn(BaseModel):
    barcode: str = Field(..., pattern=r'^\d+$')
    description_blocks: List[DescriptionBlock]
    seo: SEO
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = Field(default=False)

ProductDetailOut = ProductDetailIn
class ProductMessageOut(BaseModel):
    status: str
    message: str
    id: str
class UploadResponse(BaseModel):
    success: bool
    message: str
    new_uploaded: int
    already_exists: int

class BarcodeIn(BaseModel):
    barcode: str = Field(..., pattern=r'^\d+$')


    
# barcode: str = Field(..., pattern=r'^\d+$', min_length=6, max_length=13)