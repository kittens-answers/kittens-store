from fastapi import Request

from kittens_store.store import BaseStore


def store_depend(request: Request) -> BaseStore:
    return request.app.state.store
