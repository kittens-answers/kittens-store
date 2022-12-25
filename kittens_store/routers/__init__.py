from fastapi import FastAPI

from . import questions, tg, tg_web_hook


def init_routers(app: FastAPI):
    app.include_router(questions.router, prefix="/questions")
    app.include_router(tg.router, prefix="/tg")
    app.include_router(tg_web_hook.router, prefix="/tg")
