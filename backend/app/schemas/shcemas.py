from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserDetailResponse(UserResponse):
    profile: Optional['ProfileResponse'] = None

class ProfileBase(BaseModel):
    bio: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None

class ProfileResponse(ProfileBase):
    class Config:
        from_attributes = True

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Post Schemas
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str
    summary: Optional[str] = Field(None, max_length=500)
    published: bool = False

class PostCreate(PostBase):
    category_ids: Optional[List[int]] = None
    tag_names: Optional[List[str]] = None

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=500)
    published: Optional[bool] = None
    category_ids: Optional[List[int]] = None
    tag_names: Optional[List[str]] = None

class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int
    owner: UserResponse
    
    class Config:
        from_attributes = True

class PostDetailResponse(PostResponse):
    categories: List['CategoryResponse'] = []
    tags: List['TagResponse'] = []

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

class TagResponse(TagBase):
    id: int
    
    class Config:
        from_attributes = True

class FileBase(BaseModel):
    filename: str

class FileResponse(FileBase):
    id: int
    file_path: str
    file_size: int
    mime_type: str
    uploaded_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List

UserDetailResponse.update_forward_refs()
PostDetailResponse.update_forward_refs()