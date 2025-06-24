from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal, List
import os
from dotenv import load_dotenv
# edit evn here 
# env = os.getenv("ENV", "dev")
# env_file = ".env.production" if env == "production" else ".env.dev"
# print(f"Using environment file: {env_file}")
ENV_FILE = ".env.production" if os.getenv("ENV", "dev") == "production" else ".env.dev"
print(f"Using environment file: {ENV_FILE}")
# load_dotenv(dotenv_path=ENV_FILE, override=True)
class SettingsBase(BaseSettings):
    class Config:
        # env_file = ".env"
        # env_file = ".env"
        env_file = ENV_FILE
        extra = "ignore"
        # extra = "allow"
class ConfigDB(SettingsBase):
    """Configuration class for database settings."""
    sqlalchemy_database_uri: str = Field(..., env="SQLALCHEMY_DATABASE_URI")
    sqlalchemy_pool_size: int = Field(5, env="SQLALCHEMY_POOL_SIZE")
    sqlalchemy_max_overflow: int = Field(10, env="SQLALCHEMY_MAX_OVERFLOW")
    sqlalchemy_pool_recycle: int = Field(1800, env="SQLALCHEMY_POOL_RECYCLE")
    sqlalchemy_pool_timeout: int = Field(30, env="SQLALCHEMY_POOL_TIMEOUT")
    sqlalchemy_echo: bool = Field(False, env="SQLALCHEMY_ECHO")
    sqlalchemy_track_modifications: bool = Field(False, env="SQLALCHEMY_TRACK_MODIFICATIONS")

class MongoSettings(SettingsBase):
    mongo_uri: str = Field(..., env="MONGO_URI")
    db_name: str = Field(..., env="DB_NAME")
    max_pool_size: int = Field(100, env="MONGO_MAX_POOL_SIZE")
    min_pool_size: int = Field(10, env="MONGO_MIN_POOL_SIZE")
    connect_timeout_ms: int = Field(30000, env="MONGO_CONNECT_TIMEOUT_MS")
    server_selection_timeout_ms: int = Field(30000, env="MONGO_SERVER_SELECTION_TIMEOUT_MS")
    socket_timeout_ms: int = Field(30000, env="MONGO_SOCKET_TIMEOUT_MS")
    wait_queue_timeout_ms: int = Field(30000, env="MONGO_WAIT_QUEUE_TIMEOUT_MS")
    retry_writes: bool = Field(True, env="MONGO_RETRY_WRITES")
    write_concern: Literal["majority", "1", "0"] = Field("majority", env="MONGO_WRITE_CONCERN")
    journal: bool = Field(True, env="MONGO_JOURNAL")
    tz_aware: bool = Field(True, env="MONGO_TZ_AWARE")

class ConfigApp(SettingsBase):
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    debug: bool = Field(default=False, env="DEBUG")
    environment: Literal["development", "production"] = Field(default="development", env="ENV")
# Khởi tạo 1 biến toàn cục
class AppConfig(SettingsBase):
    access_secret_key: str = Field("your-default-secret-key", env="SECRET_KEY")
    refresh_secret_key: str = Field("your-default-refresh-secret-key", env="REFRESH_SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_seconds: int = Field(86400, env="ACCESS_TOKEN_EXPIRE")
    refresh_token_expire_seconds: int = Field(31536000, env="REFRESH_TOKEN_EXPIRE")
    secure_https: bool = Field(True, env="SECIRE_HTTPS")
    expiration_max_age: int = Field(600000, env="EXPIRATION_MAX_AGE")
    samesite: str = Field("Lax", env="SAMESITE")

class ConfigMinio(SettingsBase):
    minio_endpoint: str = Field("localhost:9000", env="MINIO_ENDPOINT")
    minio_ip_address: str = Field("localhost", env="MINIO_IP_ADDRESS")
    minio_access_key: str = Field("admin", env="MINIO_ROOT_USER")
    minio_secret_key: str = Field("admin123", env="MINIO_ROOT_PASSWORD")
    secure_https: bool = Field(False, env="MINIO_SECURE")
    minio_bucket_name: str = Field("mybucket", env="MINIO_BUCKET_NAME")


class ConfigRedis(SettingsBase):
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")
    redis_password: str | None = Field(None, env="REDIS_PASSWORD")

config_db = ConfigDB()
mongo_settings = MongoSettings()
app_config = AppConfig()
config_app = ConfigApp()
minio_config = ConfigMinio()
redis_config = ConfigRedis()

