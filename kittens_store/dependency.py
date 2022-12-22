from fastapi import Request

from kittens_store.bot import TG_App
from kittens_store.store import BaseStore


def store_depend(request: Request) -> BaseStore:
    return request.app.state.store


def tg_depend(request: Request) -> TG_App:
    return request.app.state.tg_app
