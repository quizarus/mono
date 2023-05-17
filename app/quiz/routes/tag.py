from fastapi import Depends, APIRouter

from app.quiz.dao.tag import TagEntityManager
from app.quiz.schemas.tag import TagSchema, CreateTagSchema, UpdateTagSchema

router = APIRouter()


@router.get('/', response_model=list[TagSchema])
async def get_list(manager: TagEntityManager = Depends()):
    return await manager.get_all()


@router.get('/{pk}', response_model=TagSchema)
async def get(pk: int, manager: TagEntityManager = Depends()):
    return await manager.get(pk)


@router.post('/', response_model=TagSchema, status_code=201)
async def create(schema: CreateTagSchema, manager: TagEntityManager = Depends()):
    return await manager.create(**schema.dict())


@router.patch('/{pk}', response_model=TagSchema)
async def update(pk: int, schema: UpdateTagSchema, manager: TagEntityManager = Depends()):
    return await manager.update(pk, **schema.dict(exclude_unset=True))


@router.delete('/{pk}', status_code=204)
async def delete(pk: int, manager: TagEntityManager = Depends()):
    return await manager.delete(pk)

