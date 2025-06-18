from minio import Minio
from app.core.config import minio_config
minio_client = Minio(
    minio_config.minio_endpoint,
    access_key=minio_config.minio_access_key,
    secret_key=minio_config.minio_secret_key,
    secure= minio_config.secure_https,
)
