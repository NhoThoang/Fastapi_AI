from minio import Minio
from app.core.config import ConfigMinio # Giả sử bạn đọc .env qua settings
import os

minio_client = Minio(
    ConfigMinio.MINIO_ENDPOINT,
    access_key=ConfigMinio.MINIO_ACCESS_KEY,
    secret_key=ConfigMinio.MINIO_SECRET_KEY,
    secure= ConfigMinio.SECIRE_HTTPS,  # True nếu sử dụng HTTPS
)
