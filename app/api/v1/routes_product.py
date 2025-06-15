from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import  ProductOut, ProductBase
from app.schemas.account import JsonOut
from app.crud import product as crud_product
from app.db.session import get_db
from fastapi import status
import os, shutil
from fastapi.responses import JSONResponse
from app.core.minio_client import minio_client
from uuid import uuid4
import io
from app.core.config import ConfigMinio
router = APIRouter()

@router.post("/upload_products/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductBase, session: AsyncSession = Depends(get_db)):
    return await crud_product.create_product(session, product)


# @router.post("/upload_product_image/", response_model=JsonOut, status_code=status.HTTP_200_OK)
# async def upload_product_image(
#     request: Request,
#     barcode: str = Form(...),
#     image: UploadFile = File(...),
#     session: AsyncSession = Depends(get_db)
# ):
#     username = request.cookies.get("username")
#     # # 🔍 Tìm sản phẩm theo barcode
#     # result = await session.execute(select(Products).where(Products.barcode == barcode))
#     # product = result.scalar_one_or_none()

#     # if not product:
#     #     raise HTTPException(status_code=404, detail="Product not found")

#     # # 📁 Tạo thư mục nếu chưa có
#     save_dir = f"static/{username}/product_images"
#     os.makedirs(save_dir, exist_ok=True)

#     # 📸 Lưu ảnh
#     image_filename = f"{barcode}_{image.filename}"
#     image_path = os.path.join(save_dir, image_filename)

#     with open(image_path, "wb") as buffer:
#         shutil.copyfileobj(image.file, buffer)

#     # 📝 Cập nhật image_path vào DB
#     # product.image_path = image_path
#     # await session.commit()

#     return {
#         "status": "Image uploaded successfully",
#         "message": f"/static/product_images/{image_filename}"
#     }

@router.post("/upload_product_image/", response_model=JsonOut, status_code=status.HTTP_200_OK)
async def upload_product_image(
    request: Request,
    barcode: str = Form(...),
    image: UploadFile = File(...),
    session: AsyncSession = Depends(get_db)
):
    username = request.cookies.get("username") or "guest"
    bucket_name = "user-uploads"

    # 📁 Tạo bucket nếu chưa tồn tại
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # 📸 Tạo tên file duy nhất
    extension = image.filename.split(".")[-1]
    image_filename = f"{barcode}_{uuid4().hex}.{extension}"
    object_path = f"{username}/product_images/{image_filename}"

    # 📤 Upload vào MinIO
    file_bytes = await image.read()
    file_stream = io.BytesIO(file_bytes)
    file_size = len(file_bytes)

    minio_client.put_object(
        bucket_name,
        object_path,
        file_stream,
        length=file_size,
        content_type=image.content_type
    )

    # image_url = f"http://{minio_client._endpoint}/user-uploads/{object_path}"
    image_url = f"http://{ConfigMinio.MINIO_ENDPOINT}/{bucket_name}/{object_path}"

    return {
        "status": "Image uploaded successfully",
        "message": image_url
    }

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