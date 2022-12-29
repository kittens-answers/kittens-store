from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from kittens_store.bot.config import settings
from kittens_store.data import data
from kittens_store.dependencies.init_data import InitData
from kittens_store.templates import templates

router = APIRouter()

from dataclasses import dataclass


@dataclass
class Paginator:
    has_next: bool
    has_previous: bool
    current: int
    pages: list[int | None]


@router.get("/pag", response_class=HTMLResponse)
async def paginator(request: Request):
    paginator = Paginator(
        has_next=True,
        has_previous=False,
        current=5,
        pages=[1, None, 3, 4, 5, 6, None, 12],
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
    only_correct: bool = Form(False, alias="only-correct"),
    init_data: InitData = Depends(InitData),
):
    paginator = Paginator(
        has_next=True,
        has_previous=False,
        current=5,
        pages=[1, None, 3, 4, 5, 6, None, 12],
    )
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
    return templates.TemplateResponse(
        "item.html",
        {"request": request, "questions": questions, "paginator": paginator},
    )
