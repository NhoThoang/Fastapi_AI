from uuid import uuid4
import io
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Request, Body
from fastapi.responses import JSONResponse
from app.core.minio_client import minio_client
from uuid import uuid4
import io
from pydantic import BaseModel, Field
from app.core.security import decode_access_token
from app.core.config import minio_config
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from urllib.parse import urlparse
import hashlib
import hashlib
from tempfile import SpooledTemporaryFile
from fastapi import UploadFile, HTTPException
from fastapi.concurrency import run_in_threadpool
from uuid import uuid4
from app.schemas.mysql.product import OutputImage_hash
from app.crud.mysql.product import check_image_hash_exists, check_image_hash_and_username_exists, check_barcode_exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple
from app.crud.mysql.product import insert_image_url_image_hash
from app.schemas.mysql.product import Image_hash



# from app.crud.mongo.detail_product import *
# from app.schemas.mongo.detail_product import *

# async def compute_md5(file: UploadFile) -> str:
#     content = await file.read()
#     md5_hash = hashlib.md5(content).hexdigest()
#     # sha256_hash = hashlib.sha256(content).hexdigest()
#     file.file.seek(0)
#     return md5_hash

async def stream_and_hash(file: UploadFile) -> tuple[str, SpooledTemporaryFile]:
    hash_md5 = hashlib.md5()
    temp_file = SpooledTemporaryFile()
    while True:
        chunk = await file.read(8192)
        if not chunk:
            break
        hash_md5.update(chunk)
        temp_file.write(chunk)

    file.file.seek(0)
    temp_file.seek(0)
    return hash_md5.hexdigest(), temp_file


async def upload_images_to_minio(
    session: AsyncSession,
    username: str,
    barcode: str,
    images: List[UploadFile]
) -> Tuple[int, int]:
    
    bucket_name = "product-images"
    new_uploads = 0
    already_exists = 0
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    if not await check_barcode_exists(session=session, barcode=barcode):
        raise HTTPException(status_code=404, detail="Product not found please insert product first")
    for image in images:
        image_hash, temp_file = await stream_and_hash(image)

        image_hash_mysql = await check_image_hash_exists(session=session, image_hash=image_hash)
        if image_hash_mysql:
            already_exists += 1
            if not await check_image_hash_and_username_exists(session=session,username=username,barcode=barcode, image_hash=image_hash):
                image_hash_model = Image_hash(
                    username=username,
                    barcode=barcode,
                    image_hash=image_hash_mysql.image_hash,
                    image_url=image_hash_mysql.image_url
                )
                await insert_image_url_image_hash(session, image_hash_model)
            continue
        extension = image.filename.split(".")[-1]
        image_filename = f"{barcode}_{uuid4().hex}.{extension}"
        object_path = f"{username}/{image_filename}"
        temp_file.seek(0, 2)
        file_size = temp_file.tell()
        temp_file.seek(0)
        try:
            await run_in_threadpool(
                minio_client.put_object,
                bucket_name,
                object_path,
                temp_file,
                file_size,
                image.content_type
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
        # image_url = f"https://{minio_config.minio_ip_address}:8080/images/{object_path}"
        image_url = f"http://{minio_config.minio_ip_address}:9000/{bucket_name}/{object_path}"
        image_hash_model = Image_hash(
            username=username,
            barcode=barcode,
            image_hash=image_hash,
            image_url=image_url
        )
        await insert_image_url_image_hash(session, image_hash_model)
        new_uploads += 1
    return new_uploads, already_exists


def get_object_path_from_url(url: str, bucket_name: str) -> str:
    path = urlparse(url).path  # Lấy phần /bucket/username/abc.jpg
    return path.split(f"/{bucket_name}/")[-1]

def delete_image_from_minio(bucket_name: str, object_path: str):
    try:
        minio_client.remove_object(bucket_name, object_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

# import hashlib
# from tempfile import SpooledTemporaryFile

# async def stream_and_hash(file: UploadFile):
#     hash_md5 = hashlib.md5()
#     temp_file = SpooledTemporaryFile()

#     while True:
#         chunk = await file.read(8192)
#         if not chunk:
#             break
#         hash_md5.update(chunk)
#         temp_file.write(chunk)

#     file.file.seek(0)
#     temp_file.seek(0)
#     return hash_md5.hexdigest(), temp_file


# async def upload_image_to_minio(
#     barcode: str,
#     username: str,
#     image: UploadFile,
#     session: AsyncSession
# ) -> str:
#     bucket_name = "product-images"

#     # 1. Tính md5 hash
#     file_bytes = await image.read()
#     image_hash = hashlib.md5(file_bytes).hexdigest()
#     image.file.seek(0)  # reset lại để đọc lại nếu cần

#     # 2. Kiểm tra hash đã tồn tại chưa trong DB
#     result = await session.execute(select(Image).where(Image.image_hash == image_hash))
#     existing_image = result.scalar_one_or_none()
#     if existing_image:
#         return existing_image.image_url  # ✅ Trả về link cũ nếu đã tồn tại

#     # 3. Tạo bucket nếu chưa có
#     if not minio_client.bucket_exists(bucket_name):
#         minio_client.make_bucket(bucket_name)

#     # 4. Tạo tên file mới
#     extension = image.filename.split(".")[-1]
#     image_filename = f"{barcode}_{uuid4().hex}.{extension}"
#     object_path = f"{username}/{image_filename}"

#     # 5. Chuẩn bị file stream
#     file_stream = io.BytesIO(file_bytes)
#     file_size = len(file_bytes)

#     # 6. Upload lên MinIO
#     try:
#         await run_in_threadpool(
#             minio_client.put_object,
#             bucket_name,
#             object_path,
#             file_stream,
#             file_size,
#             image.content_type
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

#     # 7. Tạo URL và lưu DB
#     image_url = f"http://{minio_config.minio_ip_address}:9000/{bucket_name}/{object_path}"

#     session.add(Image(
#         barcode=barcode,
#         username=username,
#         image_url=image_url,
#         image_hash=image_hash
#     ))
#     await session.commit()

#     return image_url

# Gọi trong async function
# await run_in_threadpool(delete_image_from_minio, bucket_name, object_path)


# from fastapi import HTTPException

# def delete_image_from_minio(bucket_name: str, object_path: str):
#     try:
#         minio_client.remove_object(bucket_name, object_path)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
# from fastapi.concurrency import run_in_threadpool
# await run_in_threadpool(delete_image_from_minio, bucket_name, object_path)
# # 
# http://192.168.5.11:9000/product-images/string/123456787_dfd791636d79495ca612b86f12b5ced4.jpg
# nginx  
# https://192.168.5.11:8080/images/string/123456787_74af85dca3fc41799b9b2fd0879e3906.jpg