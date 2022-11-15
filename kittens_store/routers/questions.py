from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from kittens_store.dependency import store_depend
from kittens_store.store import BaseStore, DBQuestionDTO, QuestionDTO


class Question(BaseModel):
    text: str
    question_type: str

    def to_dto(self):
        return QuestionDTO(text=self.text, question_type=self.question_type)


router = APIRouter()


@router.post(
    "/",
    response_model=DBQuestionDTO,
    responses={
        status.HTTP_200_OK: {"model": DBQuestionDTO},
        status.HTTP_201_CREATED: {"model": DBQuestionDTO},
    },
)
async def create(question: Question, store: BaseStore = Depends(store_depend)):
    result = await store.questions.get_or_create(dto=question.to_dto())
    if result.created:
        return JSONResponse(
            content=jsonable_encoder(result.data), status_code=status.HTTP_201_CREATED
        )
    else:
        return JSONResponse(
            content=jsonable_encoder(result.data), status_code=status.HTTP_200_OK
        )
