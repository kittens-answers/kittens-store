class QuestionError(Exception):
    ...


class QuestionDoNotExist(QuestionError):
    ...


class QuestionAlreadyExist(QuestionError):
    ...
