from fastapi import Depends, APIRouter

from app.quiz.dao.answer import AnswerEntityManager
from app.quiz.schemas.answer import AnswerSchema, CreateAnswerSchema, UpdateAnswerSchema

router = APIRouter()


@router.get('/', response_model=list[AnswerSchema])
async def get_list(manager: AnswerEntityManager = Depends()):
    return await manager.get_all()


@router.get('/{pk}', response_model=AnswerSchema)
async def get(pk: int, manager: AnswerEntityManager = Depends()):
    return await manager.get(pk)


@router.post('/', response_model=AnswerSchema, status_code=201)
async def create(schema: CreateAnswerSchema, manager: AnswerEntityManager = Depends()):
    return await manager.create(**schema.dict())


@router.patch('/{pk}', response_model=AnswerSchema)
async def update(pk: int, schema: UpdateAnswerSchema, manager: AnswerEntityManager = Depends()):
    return await manager.update(pk, **schema.dict(exclude_unset=True))


@router.delete('/{pk}', status_code=204)
async def delete(pk: int, manager: AnswerEntityManager = Depends()):
    return await manager.delete(pk)
