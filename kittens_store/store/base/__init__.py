import abc

from .question import BaseQuestionStore


class BaseStore(abc.ABC):
    questions: BaseQuestionStore

    @abc.abstractmethod
    async def startup(self):
        ...

    @abc.abstractmethod
    async def shutdown(self):
        ...
