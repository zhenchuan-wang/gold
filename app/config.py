"""
Configuration settings for the GOLD Profile Management Application.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    database_url: str = Field(
        default="postgresql://gold_user:gold_password@localhost:5432/gold_profiles",
        description="PostgreSQL database URL",
    )

    # JWT settings
    jwt_secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT token signing",
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_hours: int = Field(
        default=24, description="JWT token expiration in hours"
    )

    # File upload settings
    upload_directory: str = Field(
        default=os.path.join(os.path.dirname(__file__), "../static/uploads"),
        description="Directory for uploaded files",
    )
    max_upload_size: int = Field(
        default=5 * 1024 * 1024, description="Maximum file upload size in bytes"
    )  # 5MB
    allowed_image_types: list = Field(
        default=["image/jpeg", "image/png", "image/gif", "image/webp"],
        description="Allowed image MIME types",
    )

    # Application settings
    debug: bool = Field(default=True, description="Debug mode")
    app_name: str = Field(
        default="GOLD Profile Manager", description="Application name"
    )
    app_version: str = Field(default="1.0.0", description="Application version")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
