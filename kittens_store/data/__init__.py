from dataclasses import dataclass
import json


@dataclass
class QuestionView:
    question: str
    question_type: str
    question_id: str
    answers: list[str] | list[tuple[bool, str]] | list[tuple[str, str]]
    is_correct: bool
    is_full: bool


def data_iter():
    with open("kittens_store/data/clear_out.json") as file:
        for q in json.load(file):
            for answer in q["answers"]:
                normalize_answer = []
                if q["type_"] == "ONE" or q["type_"] == "MANY":
                    if q["all_answers"]:
                        normalize_answer = [
                            (a in answer["value"], a) for a in q["all_answers"]
                        ]
                        is_full = True
                        yield QuestionView(
                            question=q["text"],
                            question_type=q["type_"],
                            question_id=answer["id_"],
                            answers=normalize_answer,
                            is_correct=answer["is_correct"],
                            is_full=is_full,
                        )
                    else:
                        normalize_answer = [(True, a) for a in answer["value"]]
                        is_full = False
                        yield QuestionView(
                            question=q["text"],
                            question_type=q["type_"],
                            question_id=answer["id_"],
                            answers=normalize_answer,
                            is_correct=answer["is_correct"],
                            is_full=is_full,
                        )
                elif q["type_"] == "ORDER":
                    normalize_answer = answer["value"]
                    is_full = True
                    yield QuestionView(
                        question=q["text"],
                        question_type=q["type_"],
                        question_id=answer["id_"],
                        answers=normalize_answer,
                        is_correct=answer["is_correct"],
                        is_full=is_full,
                    )

data = list(data_iter())