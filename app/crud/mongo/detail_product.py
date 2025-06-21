# routes/product_detail.py

from app.models.mongo.product_detail import ProductDetail
from app.schemas.mongo.detail_product import ProductDetailIn
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
# from app.models.product_detail import ProductDetail

# async def create_product_detail(data: ProductDetailIn):
#     detail = ProductDetail(**data.model_dump())
#     # detail = ProductDetail(**data.model_dump(mode="json"))
#     await detail.insert()
#     return detail
async def check_barcode_exist(barcode: str) -> bool:
    return await ProductDetail.find_one(ProductDetail.barcode == barcode)
async def create_product_detail(data: ProductDetailIn) -> ProductDetail:
    if await check_barcode_exist(data.barcode):
        raise HTTPException(status_code=400, detail=f"Barcode {data.barcode} already exists")
    detail = ProductDetail(**data.model_dump())
    await detail.insert()
    return detail
 
async def get_product_detail(barcode: str)-> ProductDetail:
    return await ProductDetail.find_one(ProductDetail.barcode == barcode)


# skip - offset not use in mongodb
# from bson import ObjectId

# # Trang đầu tiên
# results = await Product.find().sort("-_id").limit(20).to_list()

# # Lấy tiếp trang sau:
# last_id = results[-1].id
# next_results = await Product.find(Product.id < last_id).sort("-_id").limit(20).to_list()
