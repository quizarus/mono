import asyncio
import io
import time
from pathlib import Path

import pytest
from minio import Minio

from app.config import settings
from app.quiz.si_importer.pack_loader import load, import_to_db, SIPack


def test_load_pack():
    pack_content = load('.sources/different.siq')
    assert isinstance(pack_content, SIPack)


async def test_parse_pack(si_pack_content):
    await import_to_db(si_pack_content)
    a = 1


def test_minio(minio_client):
    folder_path = Path('.temp/pack')

    # Загрузка всех файлов из папки на MinIO
    for file_path in folder_path.iterdir():
        if file_path.is_file():
            object_name = file_path.name  # Имя объекта на MinIO
            minio_client.fput_object(settings.S3_PUBLIC_BUCKET, 'pack/' + object_name, str(file_path))
    assert True


def test_minio_get_url():
    client = Minio('127.0.0.1:9000', access_key=settings.S3_ACCESS_KEY, secret_key=settings.S3_SECRET_KEY,
                   secure=settings.S3_SECURE)
    url = client.get_presigned_url('GET', 'packs', 'test_pack/logo-Maserati.jpg')

    a = 1


