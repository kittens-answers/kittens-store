from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from kittens_store.bot.config import settings
from kittens_store.data import data
from kittens_store.dependencies.init_data import InitData
from kittens_store.templates import templates


from dataclasses import dataclass
from math import ceil

router = APIRouter()


@dataclass
class Paginator:
    has_next: bool
    has_previous: bool
    current: int
    pages: list[int | None]
    page_size: int

    @staticmethod
    def from_current(current: int, total: int, page_size: int = 10):
        pages = list(range(1, ceil(total / page_size) + 1))
        return Paginator(
            has_next=current < total,
            has_previous=current < total,
            current=current,
            pages=pages,
            page_size=page_size,
        )

    def paginate(self, data: list):
        first_el = (self.current - 1) * self.page_size
        last_el = self.current * self.page_size
        return data[first_el:last_el]


@router.get("/pag", response_class=HTMLResponse)
async def paginator(request: Request):
    paginator = Paginator(
        has_next=True,
        has_previous=False,
        current=5,
        pages=[1, None, 3, 4, 5, 6, None, 12],
        page_size=10,
    )
    return templates.TemplateResponse(
        "pagination.html", {"request": request, "paginator": paginator}
    )


@router.get("/{loader_path:path}", response_class=HTMLResponse)
async def loader(request: Request, loader_path: str):
    return templates.TemplateResponse("loader.html", {"request": request})


@router.post("/search", response_class=HTMLResponse)
async def menu(
    response: Response, request: Request, init_data: InitData = Depends(InitData)
):
    if init_data.is_valid is None:
        response.headers["HX-Redirect"] = settings.TG_BOT_URL
        return
    if init_data.is_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return templates.TemplateResponse("search.html", {"request": request})


@router.post("/result", response_class=HTMLResponse)
async def test(
    response: Response,
    request: Request,
    q: str = Form(),
    p: int = Form(1),
    only_correct: bool = Form(False, alias="only-correct"),
    init_data: InitData = Depends(InitData),
):
    if init_data.is_valid is None:
        response.headers["HX-Redirect"] = settings.TG_BOT_URL
        return
    if init_data.is_valid is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if only_correct:
        questions = [
            qu for qu in data if q.lower() in qu.question.lower() and qu.is_correct
        ]
    else:
        questions = [qu for qu in data if q.lower() in qu.question.lower()]
    paginator = Paginator.from_current(current=p, total=len(questions))
    questions = paginator.paginate(questions)
    return templates.TemplateResponse(
        "item.html",
        {"request": request, "questions": questions, "paginator": paginator},
    )
