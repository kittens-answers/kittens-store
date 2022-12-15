from fastapi import FastAPI

from .base import BaseStore
from .base.dto import DBQuestionDTO, QuestionDTO, QuestionID
from .base.exceptions import QuestionAlreadyExist, QuestionDoNotExist, QuestionError
from .memory_base import MemoryStore


def init_store(app: FastAPI):
    store = MemoryStore()
    app.add_event_handler("startup", store.startup)
    app.add_event_handler("shutdown", store.shutdown)
    app.state.store = store
