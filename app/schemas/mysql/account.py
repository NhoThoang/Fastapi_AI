import re
from typing import Optional
from pydantic import BaseModel, field_validator, Field, ConfigDict
from fastapi import HTTPException, status

class Accountusername(BaseModel):
    username: str
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        # Kiểm tra độ dài của tên người dùng
        if len(v) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be at least 3 characters long"
            )
        return v
class AccountBase(BaseModel):
    username: str
    password: str
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        # Kiểm tra độ dài của tên người dùng
        if len(v) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username must be at least 3 characters long"
            )
        return v
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        # Kiểm tra độ dài của mật khẩu
        if len(v) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )
        
        # Kiểm tra mật khẩu có ít nhất một chữ cái in hoa
        if not re.search(r'[A-Z]', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter"
            )
        
        # Kiểm tra mật khẩu có ít nhất một chữ cái in thường
        if not re.search(r'[a-z]', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one lowercase letter"
            )

        # Kiểm tra mật khẩu có ít nhất một chữ số
        if not re.search(r'[0-9]', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one number"
            )

        # Kiểm tra mật khẩu có ít nhất một ký tự đặc biệt
        if not re.search(r'[@$!%*?&]', v):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one special character: @$!%*?&"
            )
        return v    

class AccountCreate(AccountBase):
    address: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=15)

class AccountLogin(AccountBase):
    device_id: Optional[str] = Field(default=None, max_length=50)
class JsonOut(BaseModel):
    status: str
    message: str
