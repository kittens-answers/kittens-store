from fastapi import FastAPI

from kittens_store.bot import init_tg_app
from kittens_store.routers import init_routers
# from kittens_store.store import init_store

app = FastAPI()
init_routers(app=app)
# init_store(app=app)
init_tg_app(app=app)
