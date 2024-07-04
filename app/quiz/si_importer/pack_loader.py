import asyncio
import io
import json
import urllib.parse
import zipfile
from asyncio import Task
from dataclasses import dataclass
from pathlib import Path
from ssl import SSLCertVerificationError, SSLError
from time import time
from timeit import timeit
from typing import NamedTuple

import httpx
import xmltodict
from fastapi import Depends
from httpx import TimeoutException
from sqlalchemy.orm import Session

from app.config import settings, minio_client
from app.database import session
from app.quiz.dao.pack import PackEntityManager
from app.quiz.models import Pack
from uuid import uuid4
import mimetypes
import magic

from app.quiz.si_importer.game_rounds_parser import parse_rounds


class SIPackSource(NamedTuple):
    path: str
    content: bytes


@dataclass
class SIPack:
    name: str
    rounds: list[dict]


def load(filname: str) -> SIPack:
    with zipfile.ZipFile(filname, 'r') as zip_file:
        pack_name = Path(zip_file.filename).stem
        files_dir_path = Path(settings.TEMP_FILES_DIR) / pack_name
        for i, file_info in enumerate(zip_file.infolist(), start=1):
            with zip_file.open(file_info) as file:
                content = file.read()

            if file_info.filename != 'content.xml':
                file_name = urllib.parse.unquote(Path(file_info.filename).stem) + Path(file_info.filename).suffix
                file_path = files_dir_path / file_name
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(content)
                continue
            struct_content = content

    return SIPack(pack_name, files_dir_path, xmltodict.parse(struct_content)['package'])


async def import_to_db(si_pack: SIPack):
    async with session() as db:
        pack_manager = PackEntityManager(db)
        rounds = parse_rounds(si_pack.schema['rounds']['round'])
        pack = await pack_manager.create(
            name=si_pack.schema['@name'],
            icon=str(Path(settings.S3_PUBLIC_BUCKET) / si_pack.name / si_pack.schema['@logo'][1:])
        )
    return pack


async def parse_pack(filename: str, file: bytes) -> SIPack:
    pack_sources: list[tuple[str, bytes]] = []
    with zipfile.ZipFile(io.BytesIO(file), 'r') as zip_file:
        for file_info in zip_file.infolist():
            with zip_file.open(file_info) as file:
                content = file.read()

            if file_info.filename == 'content.xml':
                struct_content = content
                continue
            source_path = Path(filename).stem / Path(urllib.parse.unquote(Path(file_info.filename).stem) + Path(file_info.filename).suffix)
            pack_sources.append(SIPackSource(str(source_path), content))

    return SIPack(Path(filename).stem, pack_sources, struct_content)



class PackUploader:

    def __init__(self, filename: str, file: bytes):
        self.uuid = uuid4()
        self.name: str = Path(filename).stem
        self.file: bytes = file
        self.rounds: list[dict] = []
        # self.sources: list[tuple[str, bytes]] = []
        self.schema: dict | None = None
        self.is_serialized: bool = False

    async def serialize(self):
        with zipfile.ZipFile(io.BytesIO(self.file), 'r') as zip_file:
            with zip_file.open(zip_file.NameToInfo['content.xml']) as pack_schema:
                self.schema = await self.__parse_schema(pack_schema.read())
                rounds, internal_content_links, external_content_urls = parse_rounds(self.schema['rounds']['round'])
                external_contents = await self.__get_external_content(external_content_urls)

            for file_info in zip_file.infolist():
                with zip_file.open(file_info) as file:
                    content = file.read()

                if file_info.filename == 'content.xml':
                    continue

                for uuid, contents in internal_content_links.items():
                    zip_file_name = urllib.parse.unquote(Path(file_info.filename).name)
                    for content_name, file_name in contents.items():
                        if file_name == zip_file_name:
                            external_contents.setdefault(uuid, {})
                            external_contents[uuid][content_name] = content
                            external_contents[uuid]['url'] = zip_file_name

        self.__save_content_to_s3(external_contents)
        self.__assign_urls(rounds, external_contents)
        self.rounds = rounds
        self.is_serialized = True
        return self.serialized_pack

    @property
    def serialized_pack(self):
        if not self.is_serialized:
            raise ValueError("The pack is not serialized. Run serialize method first")

        return SIPack(self.name, self.rounds)

    async def __parse_schema(self, schema: bytes):
        schema = xmltodict.parse(schema)['package']
        self.name = schema['@name']

        return schema

    def __assign_urls(self, rounds: list, contents: dict):
        for _round in rounds:
            for theme in _round['themes']:
                for question in theme['questions']:
                    question_content_data = contents.get(question['uuid'])
                    if not question_content_data:
                        continue
                    question['attachments'] = question_content_data['attachments']


    def __save_content_to_s3(self, content):
        mime = magic.Magic(mime=True)
        for uuid in content:
            content[uuid]['attachments'] = {'content': None, 'post_content': None}
            if content[uuid].get('error'):
                continue

            for content_name in ('content', 'post_content'):
                if not content[uuid].get(content_name):
                    continue

                s3_path = Path(str(self.uuid)) / Path(str(uuid4()))
                file_stream = io.BytesIO(content[uuid][content_name])
                mime_type = mime.from_buffer(file_stream.read())
                file_stream.seek(0)
                s3_obj = minio_client.put_object(settings.S3_BUCKET, str(s3_path), file_stream, length=len(content[uuid][content_name]), content_type=mime_type)
                content[uuid]['attachments'][content_name] = minio_client.get_presigned_url('GET', settings.S3_BUCKET, s3_obj.object_name)

    async def __fetch_content(self, uuid: uuid4, client: httpx.AsyncClient, url: str, content_name: str):
        start = time()

        result = {'error': None, 'url': url, content_name: None}
        try:
            response = await client.get(url, timeout=10, follow_redirects=True)
            result = result | {content_name: response.content, 'time': time() - start}
        except TimeoutException as e:
            result = result | {'error': 'timeout error'}
        except SSLError as e:
            result = result | {'error': 'ssl error'}
        except httpx.ConnectError as e:
            result = result | {'error': 'connection error'}
        except Exception as e:
            result = result | {'error': 'unexpected load error'}
        return {uuid: result}

    async def __get_external_content(self, contents: dict[uuid4, str]):
        if not contents:
            return {}

        fetch_content_tasks = []
        results = {}
        async with httpx.AsyncClient() as client:
            for uuid, content in contents.items():
                for content_name, url in content.items():
                    fetch_content_tasks.append(asyncio.create_task(self.__fetch_content(uuid, client, url, content_name)))

            done, _ = await asyncio.wait(fetch_content_tasks)
            for done_task in done:
                result = await done_task
                results = results | result

        return results


    async def save(self):
        serialized = self.serialized_pack
        a = 1
