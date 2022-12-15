from dataclasses import dataclass

QuestionID = str


@dataclass
class QuestionDTO:
    text: str
    question_type: str


@dataclass
class DBQuestionDTO(QuestionDTO):
    question_id: QuestionID


@dataclass
class GOCQuestionResult:
    data: DBQuestionDTO
    created: bool
