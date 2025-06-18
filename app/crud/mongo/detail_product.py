# routes/product_detail.py

from app.models.mongo.product_detail import ProductDetail
from app.schemas.mongo.detail_product import ProductDetailIn
# from app.models.product_detail import ProductDetail

async def create_product_detail(data: ProductDetailIn):
    detail = ProductDetail(**data.model_dump())
    # detail = ProductDetail(**data.model_dump(mode="json"))
    await detail.insert()
    return detail

async def get_product_detail(product_id: int):
    return await ProductDetail.find_one(ProductDetail.product_id == product_id)

