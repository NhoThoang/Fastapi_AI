# from pydantic import BaseModel
# from typing import Optional

# class AccountBase(BaseModel):
#     username: str
#     address: str
#     phone: str
#     active: bool
#     admin: bool

# class AccountCreate(AccountBase):
#     password: str  # khi tạo tài khoản mới cần mật khẩu

# class AccountInDB(AccountBase):
#     id: int
#     count_refresh_token: int
#     refresh_token: Optional[str]

#     class Config:
#         from_attributes = True   # để Pydantic có thể đọc object ORM trực tiếp
# class AccountUpdate(BaseModel):
#     username: Optional[str] = None
#     address: Optional[str] = None
#     phone: Optional[str] = None
#     active: Optional[bool] = None
#     admin: Optional[bool] = None

#     class Config:
#         from_attributes = True   # để Pydantic có thể đọc object ORM trực tiếp