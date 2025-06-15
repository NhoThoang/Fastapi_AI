import os
from dotenv import load_dotenv

load_dotenv() 

class ConfigDB:
    """Configuration class for database settings."""
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_POOL_SIZE = int(os.getenv("SQLALCHEMY_POOL_SIZE", 5))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", 10))
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv("SQLALCHEMY_POOL_RECYCLE", 1800))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", 30))
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() in ("true", "1", "t")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() in ("true", "1", "t")
class Config:
    """Configuration class for application settings."""
    ACCESS_SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your-default-refresh-secret-key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE", 86400))
    REFRESH_TOKEN_EXPIRE_SECONDS = int(os.getenv("REFRESH_TOKEN_EXPIRE", 31536000))  # 1 year
    SECIRE_HTTPS = os.getenv("SECIRE_HTTPS", "True").lower() in ("true", "1", "t")
    EXPIRATION_MAX_AGE = int(os.getenv("EXPIRATION_MAX_AGE", 600000))  # 10 days in seconds
    SAMESITE = os.getenv("SAMESITE", "Lax")  # Default to Lax if not set
class ConfigMinio:
    """Configuration class for Minio settings."""
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "admin")
    MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "admin123")
    SECIRE_HTTPS = os.getenv("MINIO_SECURE", "False").lower() in ("true", "1", "t")  # Default to False if not set
    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "mybucket")  # Default bucket name
class ConfigRedis:
    """Configuration class for Redis settings."""
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)  # Optional password, None if not set
