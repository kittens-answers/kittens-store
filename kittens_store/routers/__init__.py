from fastapi import FastAPI

from . import new_tg, questions, tg


def init_routers(app: FastAPI):
    app.include_router(questions.router, prefix="/questions")
    app.include_router(tg.router, prefix="/tg")
    app.include_router(new_tg.router, prefix="/new-tg")
