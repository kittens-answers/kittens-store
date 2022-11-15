from fastapi import FastAPI

from . import questions


def init_routers(app: FastAPI):
    app.include_router(questions.router, prefix="/questions")
