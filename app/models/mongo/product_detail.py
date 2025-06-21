# from typing import List, Optional
# from beanie import Document
# from pydantic import Field
# from app.schemas.mongo.product_common import DescriptionBlock, SEO

# class ProductDetail(Document):
#     barcode: int
#     images: List[str] = Field(default_factory=list)
#     description_blocks: List[DescriptionBlock] = Field(default_factory=list)
#     seo: Optional[SEO] = None

#     class Settings:
#         name = "product_details"          # Tên collection trong MongoDB



from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import List, Optional
from app.schemas.mongo.product_common import DescriptionBlock, SEO

class ProductDetail(Document):
    barcode: Indexed(str, unique=True)
    images: List[str] = Field(default_factory=list)
    description_blocks: List[DescriptionBlock] = Field(default_factory=list)
    seo: Optional[SEO] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = Field(default=False)

    class Settings:
        name = "product_details"

# 👉 Nếu bạn muốn dùng barcode là _id, cũng có thể làm được:
# class ProductDetail(Document):
#     id: int = Field(alias="_id")
#     ...