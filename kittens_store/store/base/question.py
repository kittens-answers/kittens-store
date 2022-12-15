import abc

from .dto import DBQuestionDTO, GOCQuestionResult, QuestionDTO, QuestionID


class BaseQuestionStore(abc.ABC):
    @abc.abstractmethod
    async def create(self, dto: QuestionDTO) -> DBQuestionDTO:
        ...

    @abc.abstractmethod
    async def get_by_id(self, question_id: QuestionID) -> DBQuestionDTO:
        ...

    @abc.abstractclassmethod
    async def get(self, dto: QuestionDTO) -> DBQuestionDTO:
        ...

    @abc.abstractmethod
    async def get_or_create(self, dto: QuestionDTO) -> GOCQuestionResult:
        ...

    @abc.abstractmethod
    async def update(self, dto: DBQuestionDTO) -> DBQuestionDTO:
        ...
