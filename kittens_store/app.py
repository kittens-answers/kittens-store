from fastapi import FastAPI

from kittens_store.routers import init_routers
from kittens_store.store import init_store

app = FastAPI()
init_routers(app=app)
init_store(app=app)
