import io

from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from fastapi.routing import serialize_response
from starlette.responses import JSONResponse

from app.config import settings, minio_client
from app.quiz.si_importer.pack_loader import parse_pack, PackUploader
from app.quiz.si_importer.schemas import PackSchema
from fastapi.encoders import jsonable_encoder
from fastapi.utils import create_response_field

router = APIRouter()


# @router.post('/', response_model=PackSchema, status_code=202)
@router.post('/')
async def upload_pack(file: UploadFile = File(...)):
    if file.size > settings.MAX_UPLOAD_FILE_SIZE_MB * 1024 * 1024: # TODO: вынести max file size в конфиги
        return Response('File size exceeds the maximum limit', status_code=413)

    file_content = await file.read()
    pack_uploader = PackUploader(file.filename, file_content)
    pack = await pack_uploader.serialize()

    model_field = create_response_field(name='parsed_si_pack_model', type_=PackSchema)
    response_content = await serialize_response(field=model_field, response_content=pack)
    return JSONResponse(content=response_content)
