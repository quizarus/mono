from fastapi import Depends, APIRouter
from app.quiz.dao.pack import PackEntityManager
from app.quiz.schemas.pack import CreatePackSchema, PackSchema, UpdatePackSchema
from app.quiz.schemas.question import PackQuestionsSchema

router = APIRouter()


@router.get('/', response_model=list[PackSchema])
async def get_list(manager: PackEntityManager = Depends()):
    return await manager.get_all()


@router.get('/{pk}', response_model=PackSchema)
async def get(pk: int, manager: PackEntityManager = Depends()):
    return await manager.get(pk)


@router.post('/', response_model=PackSchema, status_code=201)
async def create(schema: CreatePackSchema, manager: PackEntityManager = Depends()):
    return await manager.create(**schema.dict())


@router.patch('/{pk}', response_model=PackSchema)
async def update(pk: int, schema: UpdatePackSchema, manager: PackEntityManager = Depends()):
    return await manager.update(pk, **schema.dict(exclude_unset=True))


@router.delete('/{pk}', status_code=204)
async def delete(pk: int, manager: PackEntityManager = Depends()):
    return await manager.delete(pk)


@router.get('/{pk}/questions', response_model=PackQuestionsSchema)
async def get(pk: int, manager: PackEntityManager = Depends()):
    return await manager.get(pk, relations=['questions'])
