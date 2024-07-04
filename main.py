from fastapi import FastAPI
from minio import Minio

from app.config import initial_project, settings
from app.quiz.routes.pack import router as pack_router
from app.quiz.routes.question import router as question_router
from app.quiz.routes.answer import router as answer_router
from app.quiz.routes.tag import router as tag_router
from app.quiz.si_importer.routes import router as si_importer_router

from app.utils.exceptions import exceptions


def create_app() -> FastAPI:
    initial_project()

    app = FastAPI(
        exception_handlers=exceptions,
        redoc_url='/redoc'
    )
    return app


app = create_app()

app.include_router(pack_router, tags=['packs'], prefix='/api/quiz/packs')
app.include_router(si_importer_router, tags=['si_importer'], prefix='/api/quiz/packs/import')
app.include_router(question_router, tags=['questions'], prefix='/api/quiz/questions')
app.include_router(answer_router, tags=['answers'], prefix='/api/quiz/answers')
app.include_router(tag_router, tags=['tags'], prefix='/api/quiz/tags')
