"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = Field(None, max_length=1000)
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UserCreate(UserBase):
    """Schema for creating a new user."""

    pass


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    full_name: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = Field(None, max_length=1000)
    preferences: Optional[Dict[str, Any]] = None


class UserResponse(UserBase):
    """Schema for user response data."""

    id: UUID
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data encoded in JWT token."""

    user_id: Optional[UUID] = None


class LoginRequest(BaseModel):
    """Login request schema."""

    username: str
    password: str


class ImageCropData(BaseModel):
    """Image cropping coordinates."""

    x: float = Field(..., ge=0, description="X coordinate of crop area")
    y: float = Field(..., ge=0, description="Y coordinate of crop area")
    width: float = Field(..., gt=0, description="Width of crop area")
    height: float = Field(..., gt=0, description="Height of crop area")

    @validator("width", "height")
    def validate_dimensions(cls, v):
        if v > 5000:  # Reasonable maximum dimension
            raise ValueError("Crop dimension too large")
        return v


class ImageUploadResponse(BaseModel):
    """Response after successful image upload."""

    filename: str
    url: str
    message: str = "Image uploaded successfully"


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
