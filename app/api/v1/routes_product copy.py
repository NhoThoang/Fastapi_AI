from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.mysql.product import  ProductOut, ProductBase
from app.schemas.mysql.account import JsonOut
from app.crud.mysql import product as crud_product
from app.db.mysql.session import get_db
from fastapi import status
import os, shutil
from fastapi.responses import JSONResponse
from app.core.minio_client import minio_client
from uuid import uuid4
import io
from app.core.security import decode_access_token
from app.core.config import minio_config
from app.crud.mongo.detail_product import *
from app.crud.minio.upload_image import *
from app.schemas.mongo.detail_product import *
from app.models.mongo.product_detail import ProductDetail
import json

router = APIRouter()
from utils.hash import compute_md5  # hàm này đọc file và tính md5
from crud_product import get_image_by_hash, insert_image_hash

@router.post("/upload_products/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    request: Request,
    product_json: str = Form(...),
    images: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_db),
):
    try:
        product_data = json.loads(product_json)
        product = ProductDetailIn(**product_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid product JSON")

    username = request.cookies.get("username") or "guest"
    access_token = request.cookies.get("access_token")
    if not username or not access_token:
        raise HTTPException(status_code=400, detail="Username or access token not found in cookies")

    decoded_token = decode_access_token(access_token)
    if not decoded_token or decoded_token.get("sub") != username:
        raise HTTPException(status_code=401, detail="Invalid access token")

    image_urls = []
    image_hashes = []

    for image in images:
        # ✅ Tính hash trước khi upload
        file_bytes = await image.read()
        image_hash = hashlib.md5(file_bytes).hexdigest()
        image.file.seek(0)

        # ✅ Kiểm tra hash đã tồn tại chưa
        existing = await get_image_by_hash(session, image_hash)
        if existing:
            image_url = existing.image_url
        else:
            # ✅ Upload nếu chưa tồn tại
            file_stream = io.BytesIO(file_bytes)
            file_size = len(file_bytes)
            image_filename = f"{product.barcode}_{uuid4().hex}.{image.filename.split('.')[-1]}"
            object_path = f"{username}/{image_filename}"
            minio_client.put_object(
                "product-images",
                object_path,
                file_stream,
                length=file_size,
                content_type=image.content_type
            )
            image_url = f"https://{minio_config.minio_ip_address}:8080/images/{object_path}"
            # ✅ Lưu vào DB
            await insert_image_hash(session, barcode=product.barcode, image_hash=image_hash, image_url=image_url)

        image_urls.append(image_url)
        image_hashes.append(image_hash)

    # ✅ Ghi MongoDB (full data)
    product.images = image_urls
    product.image_hashes = image_hashes
    mongo_detail = await create_product_detail(product)

    # ✅ Ghi MySQL (basic data)
    product_base_data = {
        "name_product": product.name_product,
        "barcode": product.barcode,
        "quantity": product.quantity,
        "import_price": product.import_price,
        "sell_price": product.sell_price,
        "discount": product.discount,
        "expiry_date": product.expiry_date,
        "type_product": product.type_product,
    }
    mysql_product = ProductBase(**product_base_data)
    mysql_detail = await crud_product.create_product(session, mysql_product)

    return {
        "status": "success",
        "message": "Product detail created.",
        "id": str(mongo_detail.id)
    }


@router.post("/product_detail", response_model=ProductMessageOut, status_code=status.HTTP_200_OK)
async def product_detail(data: ProductDetailIn = Body(...)):
    detail = await create_product_detail(data)
    return {
        "status": "success",
        "message": "Product detail created.",
        "id": str(detail.id)
    }

@router.post("/upload_product_image/", response_model=JsonOut, status_code=status.HTTP_200_OK)
async def upload_product_image(
    request: Request,
    barcode: str = Form(...),
    image: UploadFile = File(...),
    session: AsyncSession = Depends(get_db)
):
    username = request.cookies.get("username") or "guest"
    access_token = request.cookies.get("access_token")
    if not username or not access_token:
        raise HTTPException(status_code=400, detail="Username or access token not found in cookies")
    # decode access_token = minio_client.decode_access_token(token=access_token) 
    decoded_token = decode_access_token(access_token)
    if not decoded_token or decoded_token.get("sub") != username:
        raise HTTPException(status_code=401, detail="Invalid access token")
    image_url = await upload_image_to_minio(barcode=barcode, username=username, image=image)

    return {
        "status": "Image uploaded successfully",
        "message": image_url
    }



@router.delete("/delete_image/")
async def delete_image(image_url: str):
    bucket_name = "product-images"
    try:
        object_path = get_object_path_from_url(image_url, bucket_name)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image URL")

    await run_in_threadpool(delete_image_from_minio, bucket_name, object_path)
    return {"detail": "Image deleted successfully"}



# @router.post("/create_full_product/", status_code=status.HTTP_201_CREATED)
# async def create_full_product(
#     request: Request,
#     # ProductBase (MySQL) fields
#     product_id: int = Form(...),
#     name: str = Form(...),
#     barcode: str = Form(...),

#     # ProductDetailIn (MongoDB) fields
#     description_blocks: str = Form(...),  # JSON string, parse sau
#     seo: str = Form(...),  # JSON string

#     # Image
#     image: UploadFile = File(...),

#     # Session for MySQL
#     session: AsyncSession = Depends(get_db)
# ):
#     # ✅ Check access_token
#     username = request.cookies.get("username") or "guest"
#     access_token = request.cookies.get("access_token")
#     if not username or not access_token:
#         raise HTTPException(status_code=400, detail="Missing credentials")
    
#     decoded_token = decode_access_token(access_token)
#     if not decoded_token or decoded_token.get("sub") != username:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     # ✅ 1. Tạo sản phẩm trong MySQL
#     product_base = ProductBase(product_id=product_id, name=name, barcode=barcode)
#     product = await crud_product.create_product(session, product_base)

#     # ✅ 2. Ghi chi tiết sản phẩm vào MongoDB
#     import json
#     try:
#         description_blocks_list = json.loads(description_blocks)
#         seo_obj = json.loads(seo)
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail="Invalid JSON in description_blocks or seo")

#     if await ProductDetail.find_one(ProductDetail.barcode == barcode):
#         raise HTTPException(status_code=409, detail="Product detail already exists")

#     detail = ProductDetail(
#         product_id=product_id,
#         barcode=barcode,
#         description_blocks=description_blocks_list,
#         seo=seo_obj
#     )
#     await detail.create()

#     # ✅ 3. Upload ảnh vào MinIO
#     extension = image.filename.split(".")[-1]
#     image_filename = f"{barcode}_{uuid4().hex}.{extension}"
#     object_path = f"{username}/product_images/{image_filename}"
#     bucket_name = "user-uploads"

#     if not minio_client.bucket_exists(bucket_name):
#         minio_client.make_bucket(bucket_name)

#     file_bytes = await image.read()
#     file_stream = io.BytesIO(file_bytes)
#     minio_client.put_object(
#         bucket_name=bucket_name,
#         object_name=object_path,
#         data=file_stream,
#         length=len(file_bytes),
#         content_type=image.content_type
#     )
#     image_url = f"http://{minio_config.minio_endpoint}/{bucket_name}/{object_path}"

#     # Optional: Update Mongo with image_url
#     await ProductDetail.find_one(ProductDetail.barcode == barcode).update({"$set": {"image_url": image_url}})

#     return {
#         "status": "success",
#         "message": "Full product created",
#         "mysql_id": product.product_id,
#         "mongo_id": str(detail.id),
#         "image_url": image_url
#     }



@router.post("/get_product_detail/", response_model=ProductDetailOut, status_code=status.HTTP_200_OK)
async def read_product_detail(barcode: BarcodeIn = Body(...)):
    detail = await get_product_detail(barcode.barcode)
    if not detail:
        raise HTTPException(status_code=404, detail="Product detail not found")
    return detail


@router.get("/info_products/", response_model=list[ProductOut], status_code=status.HTTP_200_OK)
async def get_all_products(
    request: Request,
    session: AsyncSession = Depends(get_db)):
    return await crud_product.get_products(session)

@router.get("/test_static/", status_code=status.HTTP_200_OK)
async def test_static_response():
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "This is a static response",
        }
    )
# @router.post("/product_detail", response_model= ProductDetailOut, status_code=status.HTTP_200_OK)
# async def product_detail(data: ProductDetailIn):
#     detail = await create_product_detail(data)
#     return {"status": "success", "message": "Product detail created", "id": str(detail.id)}



# @router.get("/product_image/{barcode}", response_model=JsonOut, status_code=status.HTTP_200_OK)
# async def get_product_image(
#     request: Request,
#     barcode: str,
#     session: AsyncSession = Depends(get_db)
# ):
#     # # 🔍 Tìm sản phẩm theo barcode
#     # result = await session.execute(select(Products).where(Products.barcode == barcode))
#     # product = result.scalar_one_or_none()

#     # if not product or not product.image_path:
#     #     raise HTTPException(status_code=404, detail="Product image not found")

#     # 📸 Trả về đường dẫn ảnh
#     return {
#         "status": "Image found",
#         "message": f"/static/product_images/{barcode}.jpg"
#     }   