from uuid import uuid4

from ..base.dto import DBQuestionDTO, GOCQuestionResult, QuestionDTO, QuestionID
from ..base.exceptions import QuestionAlreadyExist, QuestionDoNotExist
from ..base.question import BaseQuestionStore


class MemoryQuestionStore(BaseQuestionStore):
    def __init__(self) -> None:
        self._data: dict[QuestionID, QuestionDTO] = {}

    def _new_id(self) -> QuestionID:
        return str(uuid4())

    async def get_by_id(self, question_id: QuestionID) -> DBQuestionDTO:
        try:
            question = self._data[question_id]
            return DBQuestionDTO(
                text=question.text,
                question_type=question.question_type,
                question_id=question_id,
            )
        except KeyError:
            raise QuestionDoNotExist(f"Question with id {question_id} do not exist")

    async def create(self, dto: QuestionDTO) -> DBQuestionDTO:
        for question_id, question in self._data.items():
            if question == dto:
                raise QuestionAlreadyExist(
                    f"Question with type {dto.question_type} and text {dto.text} already exist with id {question_id}"
                )
        new_id = self._new_id()
        self._data[new_id] = dto
        return DBQuestionDTO(
            text=dto.text, question_type=dto.question_type, question_id=new_id
        )

    async def get_or_create(self, dto: QuestionDTO) -> GOCQuestionResult:
        try:
            question = await self.get(dto=dto)
            created = False
        except QuestionDoNotExist:
            question = await self.create(dto=dto)
            created = True
        return GOCQuestionResult(data=question, created=created)

    async def update(self, dto: DBQuestionDTO) -> DBQuestionDTO:
        if dto.question_id not in self._data.keys():
            raise QuestionDoNotExist(f"Question with {dto.question_id} not exist")
        self._data[dto.question_id] = QuestionDTO(
            text=dto.text, question_type=dto.question_type
        )
        return dto

    async def get(self, dto: QuestionDTO) -> DBQuestionDTO:
        for question_id, question in self._data.items():
            if question == dto:
                return DBQuestionDTO(
                    text=dto.text,
                    question_type=dto.question_type,
                    question_id=question_id,
                )
        raise QuestionDoNotExist(
            f"Question with type {dto.question_type} and text {dto.text} do not exist"
        )
