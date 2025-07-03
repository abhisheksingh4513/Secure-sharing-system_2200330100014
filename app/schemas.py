from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserType(str, Enum):
    OPS = "ops"
    CLIENT = "client"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    user_type: UserType

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SignUpResponse(BaseModel):
    message: str
    verification_url: str
    user_id: int

class EmailVerificationRequest(BaseModel):
    token: str

class FileUploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    upload_date: datetime
    message: str
    
    class Config:
        from_attributes = True

class FileListResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    upload_date: datetime
    uploader_username: str
    
    class Config:
        from_attributes = True

class DownloadResponse(BaseModel):
    download_link: str
    message: str

class ErrorResponse(BaseModel):
    detail: str
