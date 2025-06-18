from typing import List
from pydantic import BaseModel
from .product_common import DescriptionBlock, SEO

class ProductDetailIn(BaseModel):
    product_id: int
    images: List[str]
    description_blocks: List[DescriptionBlock]
    seo: SEO

class ProductDetailOut(BaseModel):
    status: str
    message: str
    id: str
