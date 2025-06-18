from typing import List, Optional
from beanie import Document
from pydantic import Field
from app.schemas.mongo.product_common import DescriptionBlock, SEO

class ProductDetail(Document):
    product_id: int
    images: List[str] = Field(default_factory=list)
    description_blocks: List[DescriptionBlock] = Field(default_factory=list)
    seo: Optional[SEO] = None

    class Settings:
        name = "product_details"          # Tên collection trong MongoDB
