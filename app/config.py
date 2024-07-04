from pathlib import Path

from minio import Minio
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOSTNAME: str

    S3_HOST: str
    S3_BUCKET: str
    S3_PUBLIC_BUCKET: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_SECURE: bool

    TEMP_FILES_DIR: str
    MAX_UPLOAD_FILE_SIZE_MB: int

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = str(Path.cwd().joinpath('.env'))


settings = Settings()


def initial_project():
    temp_dir = Path(settings.TEMP_FILES_DIR)
    if not temp_dir.exists():
        temp_dir.mkdir()


minio_client = Minio(settings.S3_HOST, access_key=settings.S3_ACCESS_KEY, secret_key=settings.S3_SECRET_KEY,
                     secure=settings.S3_SECURE)
