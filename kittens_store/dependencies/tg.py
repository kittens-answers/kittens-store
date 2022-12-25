from fastapi import Request
from telegram import Bot
from telegram.ext import Application


def tg_app(request: Request):
    _tg_app: Application = request.app.state.tg_app
    return _tg_app


def tg_bot(request: Request):
    _tg_bot: Bot = request.app.state.tg_app.bot
    return _tg_bot
