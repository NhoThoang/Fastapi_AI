from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import base64
import urllib.parse
import secrets
from app.core.config import app_config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET_KEY nên đặt trong .env
SECRET_KEY = app_config.access_secret_key
REFRESH_SECRET_KEY = app_config.refresh_secret_key
ALGORITHM = app_config.algorithm
ACCESS_TOKEN_EXPIRE_SECONDS = app_config.access_token_expire_seconds 
REFRESH_TOKEN_EXPIRE_SECONDS = app_config.refresh_token_expire_seconds


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS))
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS))
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def decode_refresh_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_csrf_token():
    return secrets.token_urlsafe(16)
def encode_username_base64(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode('utf-8')).decode('ascii')
def decode_username_base64(encoded_text: str) -> str:
    return base64.urlsafe_b64decode(encoded_text.encode('ascii')).decode('utf-8')
def encode_username_url(text: str) -> str:
    return urllib.parse.quote(text)
def decode_username_url(encoded_text: str) -> str:
    return urllib.parse.unquote(encoded_text)
