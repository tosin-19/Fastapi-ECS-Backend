import os
from functools import lru_cache
from pydantic import BaseSettings, Field, AnyUrl

class Settings(BaseSettings):
    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    MONGODB_DB: str = Field("appdb", env="MONGODB_DB")

    AWS_REGION: str = Field("us-east-1", env="AWS_REGION")
    AWS_S3_BUCKET: str = Field(..., env="AWS_S3_BUCKET")

    AWS_ACCESS_KEY_ID: str = Field(None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(None, env="AWS_SECRET_ACCESS_KEY")

    PRESIGNED_URL_EXPIRES: int = Field(3600, env="PRESIGNED_URL_EXPIRES")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
