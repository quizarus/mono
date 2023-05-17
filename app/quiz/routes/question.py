from fastapi import Depends, APIRouter

from app.quiz.dao.question import QuestionEntityManager
from app.quiz.schemas.answer import QuestionAnswersSchema
from app.quiz.schemas.question import QuestionSchema, CreateQuestionSchema, UpdateQuestionSchema

router = APIRouter()


@router.get('/', response_model=list[QuestionSchema])
async def get_list(manager: QuestionEntityManager = Depends()):
    return await manager.get_all()


@router.get('/{pk}', response_model=QuestionSchema)
async def get(pk: int, manager: QuestionEntityManager = Depends()):
    return await manager.get(pk)


@router.post('/', response_model=QuestionSchema, status_code=201)
async def create(schema: CreateQuestionSchema, manager: QuestionEntityManager = Depends()):
    return await manager.create(**schema.dict())


@router.patch('/{pk}', response_model=QuestionSchema)
async def update(pk: int, schema: UpdateQuestionSchema, manager: QuestionEntityManager = Depends()):
    return await manager.update(pk, **schema.dict(exclude_unset=True))


@router.delete('/{pk}', status_code=204)
async def delete(pk: int, manager: QuestionEntityManager = Depends()):
    return await manager.delete(pk)


@router.get('/{pk}/answers', response_model=QuestionAnswersSchema)
async def get(pk: int, manager: QuestionEntityManager = Depends()):
    return await manager.get(pk, relations=['answers'])
