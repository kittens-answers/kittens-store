from fastapi import FastAPI

from . import questions, tg


def init_routers(app: FastAPI):
    app.include_router(questions.router, prefix="/questions")
    app.include_router(tg.router, prefix="/tg")
