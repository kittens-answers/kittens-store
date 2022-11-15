from ..base import BaseStore
from .question import MemoryQuestionStore


class MemoryStore(BaseStore):
    def __init__(self) -> None:
        self.questions = MemoryQuestionStore()

    async def startup(self):
        print("memory store start up")

    async def shutdown(self):
        print("memory store shut down")
