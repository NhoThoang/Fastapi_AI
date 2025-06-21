from uuid import uuid4
import io
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Request, Body
from fastapi.responses import JSONResponse
from app.core.minio_client import minio_client
from uuid import uuid4
import io
from app.core.security import decode_access_token
from app.core.config import minio_config
# from app.crud.mongo.detail_product import *
# from app.schemas.mongo.detail_product import *

async def upload_image_to_minio(barcode: str, username: str, image: UploadFile) -> str:
    bucket_name = "product-images"
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    extension = image.filename.split(".")[-1]
    image_filename = f"{barcode}_{uuid4().hex}.{extension}"
    object_path = f"{username}/product_images/{image_filename}"

    file_bytes = await image.read()
    file_stream = io.BytesIO(file_bytes)
    file_size = len(file_bytes)

    try:
        minio_client.put_object(
            bucket_name,
            object_path,
            file_stream,
            length=file_size,
            content_type=image.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    image_url = f"http://{minio_config.minio_endpoint}/{bucket_name}/{object_path}"
    return image_url
